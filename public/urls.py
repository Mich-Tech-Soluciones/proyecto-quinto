from django.urls import path
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.public_home, name='public_home'),
    path('tienda/', views.public_shop, name='public_shop'),
    path('producto/<int:pk>/', views.public_product_detail, name='public_product_detail'),

    # Carrito (AJAX)
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<str:key>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),

    # Checkout
    path('pedido/', views.public_checkout, name='public_checkout'),
    path('pedido/confirmado/<int:pk>/', views.public_order_success, name='public_order_success'),
]
