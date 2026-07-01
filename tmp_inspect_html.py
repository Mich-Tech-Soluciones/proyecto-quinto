import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ats.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
u = User.objects.filter(username='tester').first()
u = u or User.objects.create_user(username='tester', password='secret', role='ADMIN')
client = Client()
client.force_login(u)
resp = client.get('/private/inventory/')
html = resp.content.decode('utf-8')
print('create_count', html.count('action="/private/inventory/categories/create/"'))
print('edit_form_count', html.count('id="editCategoryForm"'))
idx = html.find('action="/private/inventory/categories/create/"')
print('create_snippet', html[idx-40:idx+200] if idx != -1 else 'NOT FOUND')
idx2 = html.find('id="editCategoryForm"')
print('edit_snippet', html[idx2-40:idx2+200] if idx2 != -1 else 'NOT FOUND')
