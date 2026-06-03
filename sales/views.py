from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
import json
from inventory.models import Product, Catalog, Category, Kardex
from .models import Order, OrderDetail, Payment

class ManageSalesView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'DESIGN']

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
        # Datos Generales
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
        except:
            items = []
            
        abono = float(request.POST.get('abono', 0))
        total = sum(float(item['price']) * int(item['quantity']) for item in items)
        
        # Determine payment status
        if abono >= total:
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
            user=request.user
        )
        
        # Abono
        if abono > 0:
            Payment.objects.create(
                order=order,
                amount=abono,
                payment_method=metodo_pago,
                note='Abono Inicial',
                user=request.user
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
                unit_cost=product.cost
            )
            
            # Reduce Stock
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
                    user=request.user
                )

        return redirect('sales_pos')
