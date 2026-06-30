from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from sales.models import Order
from inventory.models import Kardex, ProductSize
from .models import ProductionSheet

class ManageProductionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'CUT', 'PRODUCTION', 'PACKAGING']

    def get(self, request):
        # Shows orders that have production sheets
        sheets = ProductionSheet.objects.all().order_by('-created_at')
        pending_orders = Order.objects.filter(production_sheet__isnull=True)
        
        context = {
            'sheets': sheets,
            'pending_orders': pending_orders,
        }
        return render(request, 'production/list.html', context)
        
    def post(self, request):
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        ProductionSheet.objects.get_or_create(order=order)
        return redirect('production_manage')

class EditProductionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'CUT', 'PRODUCTION', 'PACKAGING']

    @transaction.atomic
    def post(self, request, sheet_id):
        sheet = get_object_or_404(ProductionSheet, id=sheet_id)
        
        # 1. Update ProductionSheet fields
        sheet.status = request.POST.get('status', sheet.status)
        sheet.designed_by = request.POST.get('designed_by') or None
        sheet.produced_by = request.POST.get('produced_by') or None
        sheet.qc_by = request.POST.get('qc_by') or None
        sheet.save()
        
        # 2. Update Order detail quantities and adjust stocks
        order = sheet.order
        for item in order.details.all():
            qty_field = f'item_qty_{item.id}'
            if qty_field in request.POST:
                try:
                    new_qty = int(request.POST.get(qty_field))
                    if new_qty > 0 and new_qty != item.quantity:
                        diff = new_qty - item.quantity
                        item.quantity = new_qty
                        item.save()
                        
                        # Adjust product stock and create Kardex log
                        product = item.product
                        if product:
                            product.stock -= diff
                            product.save()
                            
                            Kardex.objects.create(
                                product=product,
                                size=item.size,
                                movement_type='Salida' if diff > 0 else 'Entrada',
                                quantity=abs(diff),
                                prev_stock=product.stock + diff,
                                new_stock=product.stock,
                                reason=f'Ajuste Cant. en Hoja #{sheet.id}',
                                user=request.user
                            )
                            
                            # Adjust size stock
                            if item.size:
                                try:
                                    ps = ProductSize.objects.get(product=product, size=item.size)
                                    ps.stock -= diff
                                    ps.save()
                                except ProductSize.DoesNotExist:
                                    pass
                except ValueError:
                    pass
                    
        # 3. Recalculate order total and update payment status
        order.total = sum(d.quantity * d.unit_price for d in order.details.all())
        
        paid = sum(p.amount for p in order.payments.all())
        if paid >= order.total:
            order.payment_status = 'Completado'
        elif paid > 0:
            order.payment_status = 'Parcial'
        else:
            order.payment_status = 'Pendiente'
            
        order.save()
        
        return redirect('production_manage')

class DeleteProductionView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'CUT', 'PRODUCTION', 'PACKAGING']

    def post(self, request, sheet_id):
        sheet = get_object_or_404(ProductionSheet, id=sheet_id)
        if sheet.status == 'Completado':
            sheet.delete()
        return redirect('production_manage')

class PrintProductionSheetView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'CUT', 'PRODUCTION', 'PACKAGING']

    def get(self, request, sheet_id):
        sheet = get_object_or_404(ProductionSheet, id=sheet_id)
        return render(request, 'production/print.html', {'sheet': sheet})
