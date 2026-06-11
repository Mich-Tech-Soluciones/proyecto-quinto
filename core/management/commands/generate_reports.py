"""
Comando de management para generar reportes
"""

from django.core.management.base import BaseCommand
from core.report_helpers import (
    generate_sales_report,
    generate_inventory_report,
    generate_production_report,
    generate_cost_report
)


class Command(BaseCommand):
    help = 'Genera reportes del sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sales',
            action='store_true',
            help='Generar reporte de ventas',
        )
        parser.add_argument(
            '--inventory',
            action='store_true',
            help='Generar reporte de inventario',
        )
        parser.add_argument(
            '--production',
            action='store_true',
            help='Generar reporte de producción',
        )
        parser.add_argument(
            '--costs',
            action='store_true',
            help='Generar reporte de costos',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Generar todos los reportes',
        )

    def handle(self, *args, **options):
        if options['all'] or options['sales']:
            self.print_sales_report()

        if options['all'] or options['inventory']:
            self.print_inventory_report()

        if options['all'] or options['production']:
            self.print_production_report()

        if options['all'] or options['costs']:
            self.print_cost_report()

        if not any(options.values()):
            self.stdout.write(
                self.style.WARNING(
                    'Use --all, --sales, --inventory, --production, or --costs'
                )
            )

    def print_sales_report(self):
        """Imprime reporte de ventas"""
        report = generate_sales_report()
        self.stdout.write(self.style.SUCCESS('\n=== SALES REPORT ==='))
        for key, value in report.items():
            self.stdout.write(f'{key}: {value}')

    def print_inventory_report(self):
        """Imprime reporte de inventario"""
        report = generate_inventory_report()
        self.stdout.write(self.style.SUCCESS('\n=== INVENTORY REPORT ==='))
        for key, value in report.items():
            self.stdout.write(f'{key}: {value}')

    def print_production_report(self):
        """Imprime reporte de producción"""
        report = generate_production_report()
        self.stdout.write(self.style.SUCCESS('\n=== PRODUCTION REPORT ==='))
        for key, value in report.items():
            self.stdout.write(f'{key}: {value}')

    def print_cost_report(self):
        """Imprime reporte de costos"""
        report = generate_cost_report()
        self.stdout.write(self.style.SUCCESS('\n=== COST REPORT ==='))
        for key, value in report.items():
            self.stdout.write(f'{key}: {value}')
