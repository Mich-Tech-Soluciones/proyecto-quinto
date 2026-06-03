from django.urls import path
from .views import ManageProductionView, PrintProductionSheetView

urlpatterns = [
    path('', ManageProductionView.as_view(), name='production_manage'),
    path('print/<int:sheet_id>/', PrintProductionSheetView.as_view(), name='production_print'),
]
