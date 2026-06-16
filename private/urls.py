from django.contrib import admin
from django.urls import path, include
from .views import dashboard_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('admin/', admin.site.urls),
    path('inventory/', include('inventory.urls')),
    path('production/', include('production.urls')),
    path('costs/', include('costs.urls')),
    path('sales/', include('sales.urls')),
    path('users/', include('users.urls')),
]
