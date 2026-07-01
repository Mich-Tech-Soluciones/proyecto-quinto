import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ats.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model
from inventory.models import Category, Catalog

User = get_user_model()
u = User.objects.filter(username='tester').first()
if not u:
    u = User.objects.create_user(username='tester', password='secret', role='ADMIN')
client = Client()
client.force_login(u)
Catalog.objects.get_or_create(name='Catálogo General', defaults={'icon': 'bi-folder'})
resp = client.post('/private/inventory/', {'action': 'create_category', 'nombre': 'CategoriaTest123'})
print('status', resp.status_code)
print('redirect', getattr(resp, 'url', None))
print('exists', Category.objects.filter(name='CategoriaTest123').exists())
