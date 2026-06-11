"""
Fixtures y datos de prueba para tests
"""

from django.contrib.auth import get_user_model
from inventory.models import Product, Catalog, Category
from sales.models import Order, OrderDetail
from decimal import Decimal

User = get_user_model()


def create_test_user(username='testuser', role='PRODUCTION'):
    """Crea un usuario de prueba"""
    return User.objects.create_user(
        username=username,
        email=f'{username}@test.com',
        password='testpass123',
        role=role
    )


def create_test_admin_user():
    """Crea un usuario administrador de prueba"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='adminpass123',
        role='ADMIN'
    )


def create_test_product():
    """Crea un producto de prueba"""
    catalog, _ = Catalog.objects.get_or_create(
        name='Test Catalog',
        defaults={'icon': 'bi-box'}
    )
    
    category, _ = Category.objects.get_or_create(
        catalog=catalog,
        name='Test Category'
    )
    
    return Product.objects.create(
        name='Test Product',
        description='A test product',
        catalog=catalog,
        category=category,
        price=Decimal('100.00'),
        cost=Decimal('50.00'),
        stock=100,
    )


def create_test_order(customer_name='Test Customer'):
    """Crea una orden de prueba"""
    user = create_test_user('salesuser', 'ADMIN')
    
    order = Order.objects.create(
        customer_name=customer_name,
        customer_email='customer@test.com',
        customer_phone='1234567890',
        total=Decimal('1000.00'),
        user=user,
    )
    
    # Agregar un detalle de orden
    product = create_test_product()
    OrderDetail.objects.create(
        order=order,
        product=product,
        quantity=10,
        unit_price=Decimal('100.00'),
        unit_cost=Decimal('50.00'),
    )
    
    return order
