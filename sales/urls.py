from django.urls import path
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from .views import (
    ManageSalesView,
    OrderListView,
    OrderCreateUpdateView,
    OrderDetailView,
    OrderDeleteView,
    SalesReportView,
)

urlpatterns = [
    # Al abrir /sales/ redirigir al historial; POS queda en /sales/pos/
    path('', RedirectView.as_view(url=reverse_lazy('sales_history'))),
    path('pos/', ManageSalesView.as_view(), name='sales_pos'),
    path('historial/', OrderListView.as_view(), name='sales_history'),
    path('historial/reporte/', SalesReportView.as_view(), name='sales_report'),
    path('orden/nuevo/', OrderCreateUpdateView.as_view(), name='order_create'),
    path('orden/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orden/<int:pk>/editar/', OrderCreateUpdateView.as_view(), name='order_update'),
    path('orden/<int:pk>/eliminar/', OrderDeleteView.as_view(), name='order_delete'),
]
