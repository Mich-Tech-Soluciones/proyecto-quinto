from django.shortcuts import render, get_object_or_404
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
        ProductionSheet.objects.create(order=order)
        return render(request, 'production/list.html', {'sheets': ProductionSheet.objects.all()})

class PrintProductionSheetView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'CUT', 'PRODUCTION', 'PACKAGING']

    def get(self, request, sheet_id):
        sheet = get_object_or_404(ProductionSheet, id=sheet_id)
        return render(request, 'production/print.html', {'sheet': sheet})
