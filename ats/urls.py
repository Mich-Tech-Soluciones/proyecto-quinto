from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', RedirectView.as_view(url='/private/admin/', permanent=False)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('public.urls')),
    path('private/', include('private.urls')),
    path('dashboard/', RedirectView.as_view(url='/private/', permanent=False)),
    path('users/', RedirectView.as_view(url='/private/users/', permanent=False)),
    path('inventory/', RedirectView.as_view(url='/private/inventory/', permanent=False)),
    path('production/', RedirectView.as_view(url='/private/production/', permanent=False)),
    path('costs/', RedirectView.as_view(url='/private/costs/', permanent=False)),
    path('sales/', RedirectView.as_view(url='/private/sales/', permanent=False)),
]
