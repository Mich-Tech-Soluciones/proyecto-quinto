"""
Vistas para la tienda pública e-commerce de Kaza.
"""
import json
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from inventory.models import Product, Catalog, Category, ProductSize
from sales.models import Order, OrderDetail


# ─── Helpers de Carrito ─────────────────────────────────────────────────────

def _get_cart(request):
    """Retorna el carrito de la sesión."""
    return request.session.get('kaza_cart', {})


def _save_cart(request, cart):
    """Persiste el carrito en sesión."""
    request.session['kaza_cart'] = cart
    request.session.modified = True


def _cart_context(cart):
    """Retorna datos de contexto del carrito para los templates."""
    total = sum(
        Decimal(str(item['price'])) * int(item['quantity'])
        for item in cart.values()
    )
    for key, item in cart.items():
        item['subtotal'] = float(
            Decimal(str(item['price'])) * int(item['quantity'])
        )
    return {
        'cart_items': cart,
        'cart_count': sum(int(i['quantity']) for i in cart.values()),
        'cart_total': f"{total:.2f}",
    }


def _base_context(request):
    """Contexto compartido para todas las páginas públicas."""
    cart = _get_cart(request)
    ctx = _cart_context(cart)
    ctx['catalogs'] = Catalog.objects.all().prefetch_related('categories')
    return ctx


# ─── Vistas Públicas ─────────────────────────────────────────────────────────

def public_home(request):
    """Página principal de la tienda."""
    ctx = _base_context(request)
    ctx['featured_products'] = Product.objects.filter(
        featured=True, stock__gt=0
    ).select_related('catalog', 'category')[:12]
    ctx['all_products'] = Product.objects.filter(
        stock__gt=0
    ).select_related('catalog', 'category')[:8]
    return render(request, 'public/home.html', ctx)


def public_shop(request):
    """Catálogo de tienda con filtros."""
    ctx = _base_context(request)

    products = Product.objects.select_related('catalog', 'category')

    # Filtro por catálogo
    catalog_id = request.GET.get('catalog')
    selected_catalog = None
    if catalog_id:
        selected_catalog = Catalog.objects.filter(pk=catalog_id).first()
        if selected_catalog:
            products = products.filter(catalog=selected_catalog)

    # Filtro por categoría
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Filtro por talla
    selected_size = request.GET.get('size')
    if selected_size:
        product_ids = ProductSize.objects.filter(
            size=selected_size, stock__gt=0
        ).values_list('product_id', flat=True)
        products = products.filter(id__in=product_ids)

    # Búsqueda
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Ordenamiento
    sort = request.GET.get('sort', 'newest')
    sort_map = {
        'newest': '-created_at',
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
    }
    products = products.order_by(sort_map.get(sort, '-created_at'))

    # Tallas disponibles para el sidebar
    available_sizes = (
        ProductSize.objects.filter(stock__gt=0)
        .values_list('size', flat=True)
        .distinct()
        .order_by('size')
    )

    # Paginación
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    ctx.update({
        'products': page_obj,
        'selected_catalog': selected_catalog,
        'search_query': search_query,
        'sort': sort,
        'available_sizes': list(available_sizes),
        'selected_size': selected_size,
    })
    return render(request, 'public/shop.html', ctx)


def public_product_detail(request, pk):
    """Detalle de un producto."""
    product = get_object_or_404(Product, pk=pk)
    ctx = _base_context(request)

    sizes = product.sizes.all().order_by('size')
    has_sizes = sizes.exists()

    # Productos relacionados (mismo catálogo, máx. 4)
    related = Product.objects.filter(
        catalog=product.catalog
    ).exclude(pk=pk).filter(stock__gt=0)[:4]

    ctx.update({
        'product': product,
        'sizes': sizes,
        'has_sizes': has_sizes,
        'related_products': related,
    })
    return render(request, 'public/product_detail.html', ctx)


# ─── Carrito (AJAX) ──────────────────────────────────────────────────────────

@require_POST
def add_to_cart(request):
    """Agrega un producto al carrito (sesión)."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Datos inválidos'}, status=400)

    product_id = str(data.get('product_id', ''))
    size = data.get('size', '').strip()
    quantity = max(1, int(data.get('quantity', 1)))

    product = get_object_or_404(Product, pk=product_id)

    # Verificar stock
    if product.stock == 0:
        return JsonResponse({'success': False, 'error': 'Producto agotado'})

    # Si tiene tallas, verificar stock de talla
    if size:
        ps = ProductSize.objects.filter(product=product, size=size).first()
        if ps and ps.stock == 0:
            return JsonResponse({'success': False, 'error': 'Talla agotada'})

    cart = _get_cart(request)
    cart_key = f"{product_id}_{size}" if size else product_id

    if cart_key in cart:
        cart[cart_key]['quantity'] = min(
            cart[cart_key]['quantity'] + quantity,
            product.stock
        )
    else:
        image_url = product.image.url if product.image else ''
        cart[cart_key] = {
            'product_id': product_id,
            'name': product.name,
            'price': float(product.price),
            'size': size,
            'quantity': quantity,
            'image': image_url,
        }

    _save_cart(request, cart)
    ctx = _cart_context(cart)

    return JsonResponse({
        'success': True,
        'cart_count': ctx['cart_count'],
        'cart_total': ctx['cart_total'],
    })


@require_POST
def remove_from_cart(request, key):
    """Elimina un ítem del carrito."""
    cart = _get_cart(request)
    cart.pop(key, None)
    _save_cart(request, cart)

    ctx = _cart_context(cart)
    return JsonResponse({
        'success': True,
        'cart_count': ctx['cart_count'],
        'cart_total': ctx['cart_total'],
    })


def cart_view(request):
    """Retorna los datos del carrito en JSON."""
    cart = _get_cart(request)
    ctx = _cart_context(cart)
    return JsonResponse({
        'cart_items': ctx['cart_items'],
        'cart_count': ctx['cart_count'],
        'cart_total': ctx['cart_total'],
    })


# ─── Checkout ────────────────────────────────────────────────────────────────

def public_checkout(request):
    """Muestra y procesa el formulario de checkout."""
    cart = _get_cart(request)
    ctx = _base_context(request)

    if request.method == 'POST' and cart:
        # Calcular total
        total = sum(
            Decimal(str(item['price'])) * int(item['quantity'])
            for item in cart.values()
        )

        # Crear la orden
        order = Order.objects.create(
            customer_name=request.POST.get('customer_name', ''),
            customer_email=request.POST.get('customer_email', '') or None,
            customer_phone=request.POST.get('customer_phone', '') or None,
            company=request.POST.get('company', '') or None,
            notes=request.POST.get('notes', '') or None,
            payment_method=request.POST.get('payment_method', 'Efectivo'),
            payment_status='Pendiente',
            status='Pendiente',
            total=total,
            user=None,
        )

        # Crear los detalles de la orden
        for key, item in cart.items():
            product = Product.objects.filter(pk=item['product_id']).first()
            OrderDetail.objects.create(
                order=order,
                product=product,
                custom_name=item['name'],
                size=item.get('size') or None,
                quantity=item['quantity'],
                unit_price=Decimal(str(item['price'])),
                unit_cost=product.cost if product else Decimal('0.00'),
            )

        # Limpiar carrito
        _save_cart(request, {})

        return redirect('public_order_success', pk=order.pk)

    # GET — mostrar formulario
    ctx.update({
        'cart_items': cart,
        'cart_total': sum(
            Decimal(str(item['price'])) * int(item['quantity'])
            for item in cart.values()
        ),
        'form_data': request.POST if request.method == 'POST' else {},
    })

    # Calcular subtotales para la vista
    for key, item in cart.items():
        item['subtotal'] = float(
            Decimal(str(item['price'])) * int(item['quantity'])
        )

    return render(request, 'public/checkout.html', ctx)


def public_order_success(request, pk):
    """Página de confirmación de pedido exitoso."""
    order = get_object_or_404(Order, pk=pk)
    ctx = _base_context(request)
    ctx['order'] = order
    return render(request, 'public/order_success.html', ctx)
