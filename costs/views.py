from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from sales.models import Order
from .models import Cost

class ManageCostsView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role == 'ADMIN'

    def get(self, request):
        costs = Cost.objects.all().order_by('-date', '-id')
        orders = Order.objects.all().order_by('-id')
        
        context = {
            'costs': costs,
            'orders': orders,
        }
        return render(request, 'costs/list.html', context)
        
    def post(self, request):
        order_id = request.POST.get('order_id')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        
        order = None
        if order_id:
            order = Order.objects.get(id=order_id)
            
        Cost.objects.create(order=order, description=description, amount=amount)
        return self.get(request)
