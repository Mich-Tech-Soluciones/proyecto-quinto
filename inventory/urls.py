from django.urls import path
from .views import ManageInventoryView

urlpatterns = [
    path('', ManageInventoryView.as_view(), name='inventory_manage'),
]
