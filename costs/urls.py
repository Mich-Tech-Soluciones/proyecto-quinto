from django.urls import path
from .views import ManageCostsView

urlpatterns = [
    path('', ManageCostsView.as_view(), name='costs_manage'),
]
