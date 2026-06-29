from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from sales.models import Order
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

    def post(self, request, sheet_id):
        sheet = get_object_or_404(ProductionSheet, id=sheet_id)
        sheet.status = request.POST.get('status', sheet.status)
        sheet.designed_by = request.POST.get('designed_by') or None
        sheet.produced_by = request.POST.get('produced_by') or None
        sheet.qc_by = request.POST.get('qc_by') or None
        sheet.save()
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
