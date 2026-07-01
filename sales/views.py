from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Q, Sum
import json
from inventory.models import Product, Catalog, Category, Kardex
from .models import Order, OrderDetail, Payment
from .forms import OrderForm


class SalesPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'DESIGN']


class ManageSalesView(SalesPermissionMixin, View):
    def get(self, request):
        products = Product.objects.filter(stock__gt=0).order_by('catalog', 'category', 'name')
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

        abono = float(request.POST.get('abono', 0) or 0)
        total = sum(float(item['price']) * int(item['quantity']) for item in items)

        if abono >= total and total > 0:
            payment_status = 'Completado'
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

        context = {
            'orders': orders,
            'query': query,
            'status': status,
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
        form = OrderForm(request.POST, request.FILES, instance=order)

        if form.is_valid():
            order = form.save(commit=False)
            if not order.pk:
                order.user = request.user
            order.save()
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
