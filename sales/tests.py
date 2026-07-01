import json

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from inventory.models import Catalog, Category, Product
from .models import Order, OrderDetail, Payment


class SalesTestBase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='admin', password='testpass', role='ADMIN')
        self.client = Client()
        self.client.force_login(self.user)

        self.catalog = Catalog.objects.create(name='CatTest')
        self.category = Category.objects.create(catalog=self.catalog, name='CatItem')
        self.product = Product.objects.create(
            name='Producto Test',
            price=100.00,
            cost=60.00,
            stock=5,
            catalog=self.catalog,
            category=self.category,
        )


class OrderModelTests(SalesTestBase):
    def test_paid_amount_and_balance(self):
        order = Order.objects.create(
            customer_name='Cliente Test',
            total=200.00,
            payment_method='Efectivo',
            payment_status='Pendiente',
            status='Pendiente',
            user=self.user,
        )
        Payment.objects.create(order=order, amount=70.00, payment_method='Efectivo', user=self.user)

        self.assertEqual(order.paid_amount, 70.00)
        self.assertEqual(order.balance, 130.00)

    def test_string_representation_when_product_removed(self):
        order = Order.objects.create(
            customer_name='Cliente Test',
            total=100.00,
            payment_method='Efectivo',
            payment_status='Pendiente',
            status='Pendiente',
            user=self.user,
        )
        detail = OrderDetail.objects.create(
            order=order,
            product=self.product,
            size='M',
            quantity=1,
            unit_price=100.00,
            unit_cost=60.00,
        )
        self.product.delete()
        detail.refresh_from_db()

        self.assertIn('Producto eliminado', str(detail))


class SalesViewTests(SalesTestBase):
    def test_pos_page_loads_for_authorized_user(self):
        response = self.client.get(reverse('sales_pos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detalle de la Venta')
        self.assertContains(response, self.product.name)

    def test_sales_pos_creates_order_and_reduces_stock(self):
        cart_data = [
            {
                'id': self.product.id,
                'name': self.product.name,
                'price': '100.00',
                'quantity': 1,
                'size': 'M',
            }
        ]
        response = self.client.post(reverse('sales_pos'), {
            'nombre': 'Cliente Demo',
            'telefono': '12345678',
            'email': 'demo@test.com',
            'empresa': 'Demo S.A.',
            'metodo_pago': 'Efectivo',
            'estado': 'Pendiente',
            'especificaciones': 'Test',
            'cart_data': json.dumps(cart_data),
            'abono': '40.00',
        })

        self.assertRedirects(response, reverse('sales_history'))
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.customer_name, 'Cliente Demo')
        self.assertEqual(order.payment_status, 'Parcial')
        self.assertEqual(order.paid_amount, 40.00)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 4)

    def test_sales_history_page_shows_orders(self):
        Order.objects.create(
            customer_name='Cliente Historia',
            total=50.00,
            payment_method='Efectivo',
            payment_status='Pendiente',
            status='Pendiente',
            user=self.user,
        )
        response = self.client.get(reverse('sales_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Historial de Ventas')

    def test_order_detail_page_displays_order(self):
        order = Order.objects.create(
            customer_name='Cliente Detalle',
            total=100.00,
            payment_method='Efectivo',
            payment_status='Pendiente',
            status='Pendiente',
            user=self.user,
        )
        response = self.client.get(reverse('order_detail', args=[order.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detalle de Orden')
        self.assertContains(response, 'Cliente Detalle')

    def test_order_create_view_saves_order_with_cart(self):
        cart_data = [
            {
                'id': self.product.id,
                'name': self.product.name,
                'price': '100.00',
                'quantity': 1,
                'size': 'M',
            }
        ]
        response = self.client.post(reverse('order_create'), {
            'customer_name': 'Cliente Form',
            'company': 'Empresa X',
            'payment_method': 'Efectivo',
            'payment_status': 'Pendiente',
            'status': 'Pendiente',
            'cart_data': json.dumps(cart_data),
            'abono': '20.00',
        })

        # Debe redirigir a detalle
        self.assertEqual(response.status_code, 302)
        order = Order.objects.filter(customer_name='Cliente Form').first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total, 100.00)
        self.assertEqual(order.paid_amount, 20.00)
