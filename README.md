# Kaza - Sistema de Gestión de Producción y Ventas

## Descripción

Kaza es un sistema web integral de gestión de producción y ventas desarrollado con Django. Está diseñado para empresas que necesitan administrar:

- **Inventario**: Gestión de productos, catálogos y categorías
- **Producción**: Seguimiento de órdenes de producción y hojas de producción
- **Ventas**: Administración de órdenes y pagos de clientes
- **Costos**: Registro y análisis de costos de producción
- **Usuarios**: Control de acceso basado en roles

## Características

- ✅ Autenticación de usuarios con roles personalizados
- ✅ Gestión completa de inventario
- ✅ Sistema de órdenes y pagos
- ✅ Hojas de producción con seguimiento de estado
- ✅ Registro de kardex para movimientos de inventario
- ✅ Análisis de costos
- ✅ Panel de control administrativo
- ✅ Reportes y estadísticas

## Instalación

### Requisitos
- Python 3.8+
- Django 6.0+
- PostgreSQL o SQLite

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd proyecto-quinto
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Iniciar datos de prueba (opcional)**
```bash
python manage.py init_data --all
```

8. **Ejecutar servidor**
```bash
python manage.py runserver
```

## Estructura del Proyecto

```
proyecto-quinto/
├── kaza/                 # Configuración principal
├── core/                 # Módulo core con utilidades
├── users/                # Módulo de usuarios
├── inventory/            # Módulo de inventario
├── production/           # Módulo de producción
├── sales/                # Módulo de ventas
├── costs/                # Módulo de costos
├── dashboard/            # Panel de control
├── templates/            # Templates HTML
├── static/               # Archivos estáticos
└── manage.py             # Script de Django
```

## Roles de Usuario

- **ADMIN**: Acceso total al sistema
- **DESIGN**: Acceso a diseño y producción
- **CUT**: Acceso al área de corte
- **PRODUCTION**: Acceso a producción general
- **PACKAGING**: Acceso a empaquetado

## Comandos Útiles

### Inicializar datos
```bash
python manage.py init_data --all
```

### Generar reportes
```bash
python manage.py generate_reports --all
```

### Crear migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## API y Utilidades

### Helpers de Utilidad

El módulo `core` incluye varios helpers útiles:

- **Cache Helpers**: Gestión de caché
- **Email Helpers**: Envío de emails
- **Report Helpers**: Generación de reportes
- **Form Helpers**: Utilidades para formularios
- **Date Helpers**: Manipulación de fechas

### Decoradores Personalizados

- `@admin_required`: Solo para administradores
- `@production_staff_required`: Solo para personal de producción

### Mixins para Vistas

- `AdminRequiredMixin`: Verifica acceso administrativo
- `ProductionStaffMixin`: Verifica acceso de producción
- `DateFilterMixin`: Agrega filtrado por fecha

## Testing

Ejecutar tests:
```bash
python manage.py test
```

Con cobertura:
```bash
coverage run --source='.' manage.py test
coverage report
```

## Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

Este proyecto está bajo licencia propietaria.
