"""
Comando de management para inicializar datos de prueba
"""

from django.core.management.base import BaseCommand
from core.test_fixtures import (
    create_test_user,
    create_test_admin_user,
    create_test_product,
    create_test_order
)


class Command(BaseCommand):
    help = 'Inicializa datos de prueba en la base de datos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-users',
            action='store_true',
            help='Crear usuarios de prueba',
        )
        parser.add_argument(
            '--create-products',
            action='store_true',
            help='Crear productos de prueba',
        )
        parser.add_argument(
            '--create-orders',
            action='store_true',
            help='Crear órdenes de prueba',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Crear todos los datos de prueba',
        )

    def handle(self, *args, **options):
        if options['all'] or options['create_users']:
            self.create_users()

        if options['all'] or options['create_products']:
            self.create_products()

        if options['all'] or options['create_orders']:
            self.create_orders()

        if not any(options.values()):
            self.stdout.write(
                self.style.WARNING(
                    'Use --all, --create-users, --create-products, or --create-orders'
                )
            )

    def create_users(self):
        """Crea usuarios de prueba"""
        try:
            create_test_admin_user()
            self.stdout.write(self.style.SUCCESS('✓ Admin user created'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating admin: {e}'))

        for role in ['DESIGN', 'CUT', 'PRODUCTION', 'PACKAGING']:
            try:
                create_test_user(f'user_{role.lower()}', role)
                self.stdout.write(self.style.SUCCESS(f'✓ {role} user created'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error creating {role} user: {e}'))

    def create_products(self):
        """Crea productos de prueba"""
        try:
            for i in range(5):
                product = create_test_product()
                product.name = f'Test Product {i+1}'
                product.save()
            self.stdout.write(self.style.SUCCESS('✓ Products created'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating products: {e}'))

    def create_orders(self):
        """Crea órdenes de prueba"""
        try:
            for i in range(3):
                create_test_order(f'Test Customer {i+1}')
            self.stdout.write(self.style.SUCCESS('✓ Orders created'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating orders: {e}'))
