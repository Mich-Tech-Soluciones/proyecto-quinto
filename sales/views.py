from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Q, Sum
import json
from decimal import Decimal
from django.contrib import messages


def _parse_decimal(value, default='0.00'):
    """Parsea valores a Decimal de forma segura."""
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal(str(default))
from inventory.models import Product, Catalog, Category, Kardex
from .models import Order, OrderDetail, Payment
from .forms import OrderForm


class SalesPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        # Simplificar permisos: permitir a cualquier usuario autenticado
        return True


class ManageSalesView(SalesPermissionMixin, View):
    def get(self, request):
        # Servir la interfaz POS para agregar productos al carrito
        products = Product.objects.filter(stock__gt=0).order_by('name')
        catalogs = Catalog.objects.all()
        categories = Category.objects.all()

        context = {
            'products': products,
            'catalogs': catalogs,
            'categories': categories,
        }
        return render(request, 'sales/pos.html', context)

    @transaction.atomic
    def post(self, request):
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        empresa = request.POST.get('empresa')

        metodo_pago = request.POST.get('metodo_pago')
        estado = request.POST.get('estado')
        especificaciones = request.POST.get('especificaciones')
        diseno_img = request.FILES.get('diseno_img')

        cart_data = request.POST.get('cart_data', '[]')
        try:
            items = json.loads(cart_data)
        except Exception:
            items = []

        if not items:
            messages.error(request, 'Debes agregar productos al carrito antes de confirmar la venta.')
            return redirect('sales_pos')

        # Validación: impedir crear la orden si algún producto tiene stock insuficiente
        insufficient = []
        for item in items:
            try:
                product = Product.objects.get(id=item.get('id'))
            except Product.DoesNotExist:
                product = None
            qty = int(item.get('quantity', 0) or 0)
            if product and (product.stock or 0) < qty:
                insufficient.append(f"{product.name} (disponible: {product.stock}, requerido: {qty})")

        if insufficient:
            messages.error(request, 'Stock insuficiente para: ' + ', '.join(insufficient))
            return redirect('sales_pos')

        abono = float(request.POST.get('abono', 0) or 0)
        total = sum(float(item['price']) * int(item['quantity']) for item in items)

        if abono >= total and total > 0:
            payment_status = 'Completado'
            estado = 'Pagado'
        elif abono > 0:
            payment_status = 'Parcial'
        else:
            payment_status = 'Pendiente'

        order = Order.objects.create(
            customer_name=nombre,
            customer_phone=telefono,
            customer_email=email,
            company=empresa,
            total=total,
            payment_method=metodo_pago,
            payment_status=payment_status,
            status=estado,
            technical_specs=especificaciones,
            design_image=diseno_img,
            user=request.user,
        )

        if abono > 0:
            Payment.objects.create(
                order=order,
                amount=abono,
                payment_method=metodo_pago,
                note='Abono Inicial',
                user=request.user,
            )

        for item in items:
            product = Product.objects.get(id=item['id'])
            qty = int(item['quantity'])
            OrderDetail.objects.create(
                order=order,
                product=product,
                size=item.get('size', ''),
                quantity=qty,
                unit_price=item['price'],
                unit_cost=getattr(product, 'cost', 0),
            )

            if product.stock >= qty:
                prev_stock = product.stock
                product.stock -= qty
                product.save()
                Kardex.objects.create(
                    product=product,
                    movement_type='Salida',
                    quantity=qty,
                    prev_stock=prev_stock,
                    new_stock=product.stock,
                    reason=f'Venta POS (Pedido #{order.id})',
                    user=request.user,
                )

        return redirect('sales_history')


class OrderListView(SalesPermissionMixin, View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        status = request.GET.get('status', '')
        orders = Order.objects.all()

        if query:
            orders = orders.filter(
                Q(customer_name__icontains=query)
                | Q(customer_email__icontains=query)
                | Q(company__icontains=query)
                | Q(id__icontains=query)
            )

        if status:
            orders = orders.filter(status=status)

        orders = orders.order_by('-created_at').select_related('user')
        total_orders = orders.count()

        context = {
            'orders': orders,
            'query': query,
            'status': status,
            'total_orders': total_orders,
        }
        return render(request, 'sales/sale_list.html', context)


class OrderCreateUpdateView(SalesPermissionMixin, View):
    def get(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk) if pk else None
        form = OrderForm(instance=order)
        context = {
            'form': form,
            'order': order,
        }
        return render(request, 'sales/sale_form.html', context)

    def post(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk) if pk else None
        post_data = request.POST.copy()
        if order is not None:
            if not post_data.get('payment_method'):
                post_data['payment_method'] = order.payment_method or 'Efectivo'
            if not post_data.get('payment_status'):
                post_data['payment_status'] = order.payment_status or 'Pendiente'
            if not post_data.get('status'):
                post_data['status'] = order.status or 'Pendiente'
        form = OrderForm(post_data, request.FILES, instance=order)
        is_edit = pk and order is not None

        if form.is_valid():
            # Procesar carrito si viene en el formulario (JSON)
            cart_data = request.POST.get('cart_data', '[]')
            try:
                items = json.loads(cart_data)
            except Exception:
                items = []

            abono = _parse_decimal(request.POST.get('abono', ''), default='0.00')

            # calcular total desde items si hay items
            total = Decimal('0.00')
            for it in items:
                price = _parse_decimal(it.get('price', '0'), default='0')
                qty = int(it.get('quantity', 0) or 0)
                total += price * qty

            # Antes de guardar, validar stock disponible (considerando restauración si es edición)
            # Construir mapping de cantidades previas por producto cuando se edita
            prev_qty_map = {}
            if is_edit:
                for prev in order.details.all():
                    if prev.product:
                        prev_qty_map[prev.product.id] = prev_qty_map.get(prev.product.id, 0) + prev.quantity

            # Validar cada item
            insufficient = []
            for it in items:
                try:
                    product = Product.objects.get(id=it.get('id'))
                except Product.DoesNotExist:
                    product = None
                qty = int(it.get('quantity', 0) or 0)
                available = (product.stock or 0) + (prev_qty_map.get(product.id, 0) if product else 0)
                if product and available < qty:
                    insufficient.append(f"{product.name} (disponible: {available}, requerido: {qty})")

            if insufficient:
                messages.error(request, 'Stock insuficiente para: ' + ', '.join(insufficient))
                context = {'form': form, 'order': order}
                return render(request, 'sales/sale_form.html', context)

            order = form.save(commit=False)
            if not order.pk:
                order.user = request.user

            if order.payment_status == 'Completado':
                order.status = 'Pagado'
            elif order.status == 'Pagado' and order.payment_status != 'Completado':
                order.payment_status = 'Completado'

            # si vinieron items, asignar total calculado
            if items:
                order.total = total

            # validar abono
            if abono > order.total:
                abono = order.total
                messages.warning(request, 'El abono no puede ser mayor al total; se ajustó al total de la orden.')

            order.save()

            # Si estamos editando y hay items nuevos, restaurar stock de detalles previos antes de rehacer
            if is_edit and items:
                for prev in order.details.all():
                    if prev.product:
                        prev_prod = prev.product
                        prev_prod.stock = (prev_prod.stock or 0) + prev.quantity
                        prev_prod.save()
                order.details.all().delete()

            # Registrar pago inicial si aplica
            if abono > Decimal('0.00'):
                Payment.objects.create(
                    order=order,
                    amount=abono,
                    payment_method=order.payment_method,
                    note='Abono inicial (registro manual)',
                    user=request.user,
                )

            # Crear detalles y actualizar stock y kardex
            for it in items:
                try:
                    product = Product.objects.get(id=it.get('id'))
                except Product.DoesNotExist:
                    product = None

                qty = int(it.get('quantity', 0) or 0)
                unit_price = _parse_decimal(it.get('price', '0'), default='0')

                OrderDetail.objects.create(
                    order=order,
                    product=product,
                    size=it.get('size', ''),
                    quantity=qty,
                    unit_price=unit_price,
                    unit_cost=getattr(product, 'cost', Decimal('0.00')) if product else Decimal('0.00'),
                )

                if product and product.stock >= qty:
                    prev_stock = product.stock
                    product.stock -= qty
                    product.save()
                    Kardex.objects.create(
                        product=product,
                        movement_type='Salida',
                        quantity=qty,
                        prev_stock=prev_stock,
                        new_stock=product.stock,
                        reason=f'Venta (Pedido #{order.id})',
                        user=request.user,
                    )

            messages.success(request, 'Orden guardada correctamente.')
            # Si se pidió guardar y crear nuevo, redirigir a creación
            if request.POST.get('save_and_new'):
                return redirect('order_create')
            if is_edit:
                return redirect('sales_history')
            return redirect('order_detail', pk=order.pk)

        context = {
            'form': form,
            'order': order,
        }
        return render(request, 'sales/sale_form.html', context)


class OrderDetailView(SalesPermissionMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        context = {
            'order': order,
        }
        return render(request, 'sales/order_detail.html', context)


class OrderDeleteView(SalesPermissionMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'sales/order_confirm_delete.html', {'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        messages.success(request, 'Orden eliminada correctamente.')
        return redirect('sales_history')


class SalesReportView(SalesPermissionMixin, View):
    def get(self, request):
        orders = Order.objects.all()
        total_sales = orders.aggregate(total=Sum('total'))['total'] or 0
        total_completed = orders.filter(payment_status='Completado').aggregate(total=Sum('total'))['total'] or 0
        total_pending = orders.filter(payment_status__in=['Pendiente', 'Parcial']).aggregate(total=Sum('total'))['total'] or 0
        total_orders = orders.count()
        recent_orders = orders.order_by('-created_at')[:10]

        context = {
            'summary': {
                'total_sales': total_sales,
                'completed_sales': total_completed,
                'pending_sales': total_pending,
                'order_count': total_orders,
            },
            'recent_orders': recent_orders,
        }
        return render(request, 'sales/report.html', context)
