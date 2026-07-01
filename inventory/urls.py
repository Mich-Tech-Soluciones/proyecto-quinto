from django.urls import path
from .views import (
    ManageInventoryView,
    EditProductView,
    DeleteProductView,
    CreateCategoryView,
    EditCategoryView,
    DeleteCategoryView,
)

urlpatterns = [
    path('', ManageInventoryView.as_view(), name='inventory_manage'),
    path('categories/create/', CreateCategoryView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', EditCategoryView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', DeleteCategoryView.as_view(), name='category_delete'),
    path('edit/<int:pk>/', EditProductView.as_view(), name='product_edit'),
    path('delete/<int:pk>/', DeleteProductView.as_view(), name='product_delete'),
]
