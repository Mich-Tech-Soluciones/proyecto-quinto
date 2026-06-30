from django.urls import path
from .views import ManageProductionView, PrintProductionSheetView, EditProductionView, DeleteProductionView

urlpatterns = [
    path('', ManageProductionView.as_view(), name='production_manage'),
    path('print/<int:sheet_id>/', PrintProductionSheetView.as_view(), name='production_print'),
    path('edit/<int:sheet_id>/', EditProductionView.as_view(), name='production_edit'),
    path('delete/<int:sheet_id>/', DeleteProductionView.as_view(), name='production_delete'),
]
