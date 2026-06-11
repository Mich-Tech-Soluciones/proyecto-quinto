"""
Utilidades para tests unitarios
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseTestCase(TestCase):
    """Caso base para tests"""
    
    def setUp(self):
        """Configura el test"""
        self.client = Client()
        self.admin_user = self.create_admin_user()
        self.normal_user = self.create_normal_user()
    
    def create_admin_user(self, username='admin', email='admin@test.com'):
        """Crea un usuario administrador para tests"""
        return User.objects.create_superuser(
            username=username,
            email=email,
            password='testpass123',
            role='ADMIN'
        )
    
    def create_normal_user(self, username='testuser', email='test@test.com', role='PRODUCTION'):
        """Crea un usuario normal para tests"""
        return User.objects.create_user(
            username=username,
            email=email,
            password='testpass123',
            role=role
        )
    
    def login(self, user):
        """Inicia sesión con un usuario"""
        self.client.login(username=user.username, password='testpass123')
    
    def logout(self):
        """Cierra sesión"""
        self.client.logout()
    
    def assert_status_code(self, url, expected_status, method='get'):
        """Verifica código de estado de una URL"""
        response = getattr(self.client, method)(url)
        self.assertEqual(response.status_code, expected_status)
    
    def assert_logged_in(self):
        """Verifica que hay un usuario logueado"""
        self.assertIsNotNone(self.client.session.get('_auth_user_id'))


class APITestCase(TestCase):
    """Caso base para tests de API"""
    
    def setUp(self):
        """Configura el test de API"""
        self.client = Client()
    
    def get_auth_headers(self, token):
        """Retorna headers de autenticación"""
        return {'HTTP_AUTHORIZATION': f'Token {token}'}
    
    def assert_api_response(self, response, status_code, has_data=True):
        """Verifica una respuesta de API"""
        self.assertEqual(response.status_code, status_code)
        if has_data:
            self.assertIn('content-type', response)
