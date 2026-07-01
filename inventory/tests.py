from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Catalog, Category


class CategoryCrudTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin_test',
            password='secret123',
            role='ADMIN',
        )
        self.catalog = Catalog.objects.create(name='Catálogo Principal', icon='bi-folder')
        self.client.force_login(self.user)

    def test_create_category(self):
        response = self.client.post(reverse('category_create'), {'nombre': 'Nueva Categoría'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inventory_manage'))
        self.assertTrue(Category.objects.filter(name='Nueva Categoría', catalog=self.catalog).exists())

    def test_edit_category(self):
        category = Category.objects.create(name='Vieja', catalog=self.catalog)

        response = self.client.post(reverse('category_edit', args=[category.pk]), {'nombre': 'Actualizada'})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inventory_manage'))
        category.refresh_from_db()
        self.assertEqual(category.name, 'Actualizada')

    def test_delete_category(self):
        category = Category.objects.create(name='Para Eliminar', catalog=self.catalog)

        response = self.client.post(reverse('category_delete', args=[category.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inventory_manage'))
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())
