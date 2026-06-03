from django.contrib import admin
from django.urls import path, include
from dashboard.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard_view, name='dashboard'),
    path('inventory/', include('inventory.urls')),
    path('production/', include('production.urls')),
    path('costs/', include('costs.urls')),
    path('sales/', include('sales.urls')),
    path('users/', include('users.urls')),
]
