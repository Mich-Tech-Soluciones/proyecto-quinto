# Kaza Stylus — Sistema de Gestión

Plataforma web para la gestión interna y venta pública de **Kaza Stylus**.

---

## Estructura del Proyecto

```
proyecto-quinto/
│
├── ats/                    # Configuración principal Django (settings, urls, wsgi)
├── core/                   # Utilidades y helpers compartidos
│
├── inventory/              # App: Inventario (productos, catálogos, tallas, kardex)
├── sales/                  # App: Ventas (órdenes, detalles, pagos)
├── production/             # App: Producción (hojas de producción)
├── costs/                  # App: Costos y márgenes
├── dashboard/              # App: Dashboard administrativo
├── users/                  # App: Gestión de usuarios y roles
├── public/                 # App: Tienda pública e-commerce (Kaza Stylus)
├── private/                # App: Panel de gestión administrativo (acceso restringido)
│
├── templates/
│   ├── base.html                  # Base del panel administrativo
│   ├── costs/                     # Templates de costos
│   ├── inventory/                 # Templates de inventario
│   ├── production/                # Templates de producción
│   ├── sales/                     # Templates de ventas
│   ├── users/                     # Templates de usuarios
│   ├── private/                   # Templates del panel privado
│   ├── registration/              # Login / autenticación
│   ├── public/                    # Templates de la tienda pública
│   │   ├── base_public.html       # Base oscura minimalista (Kaza Stylus)
│   │   ├── home.html              # Página de inicio con carrusel
│   │   ├── shop.html              # Catálogo de productos
│   │   ├── product_detail.html    # Detalle de producto
│   │   ├── checkout.html          # Carrito y pedido
│   │   └── order_success.html     # Confirmación de pedido
│   └── _essence-original/         # Plantilla HTML base original (referencia, no editar)
│
├── static/
│   ├── css/
│   │   └── admin.css              # Estilos del panel administrativo (paleta oscura)
│   ├── img/                       # Logos y assets del sistema
│   └── essence/                   # Assets CSS/JS/img de la tienda pública
│
├── media/                         # Archivos subidos (imágenes de productos, diseños)
├── venv/                          # Entorno virtual Python (no versionar)
└── manage.py
```

---

## URLs del Sistema

| URL | Descripción |
|-----|------------|
| `http://127.0.0.1:8000/` | Tienda pública Kaza Stylus |
| `http://127.0.0.1:8000/tienda/` | Catálogo de productos |
| `http://127.0.0.1:8000/pedido/` | Carrito / Checkout |
| `http://127.0.0.1:8000/accounts/login/` | Login del panel administrativo |
| `http://127.0.0.1:8000/private/` | Panel de gestión (requiere autenticación) |

---

## Paleta de Colores (Kaza Stylus)

| Variable | Color | Uso |
|----------|-------|-----|
| `--dark-bg` | `#111111` | Fondo principal |
| `--ats-cream` | `#F2E8C6` | Acento dorado crema |
| `--text-main` | `#ffffff` | Texto principal |
| `--text-muted` | `rgba(255,255,255,0.45)` | Texto secundario |
| `--dark-card` | `rgba(255,255,255,0.04)` | Tarjetas glassmorphism |

---

## Ejecutar el Servidor

```bash
# Activar entorno virtual
venv\Scripts\activate

# Iniciar servidor de desarrollo
python manage.py runserver 8000
```

---
## Integrantes

Sofia Chamorro
Alvaro Chogllo
Abigail Topanata
Camila Tuso
Edson Venegas

Proyecto desarrollado con Django y PostgreSQL para la gestión de Kaza Stylus.
*Kaza Stylus — Moda & Estilo © 2025*
