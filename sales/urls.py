from django.urls import path
from .views import ManageSalesView

urlpatterns = [
    path('', ManageSalesView.as_view(), name='sales_pos'),
]
