from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Product, Catalog, Category, ProductSize, Kardex


class CategoryBaseView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'DESIGN']

    def get_catalog(self):
        return Catalog.objects.first() or Catalog.objects.create(name='Catálogo General', icon='bi-folder')


class CreateCategoryView(CategoryBaseView):
    def post(self, request):
        name = request.POST.get('nombre', '').strip()
        if not name:
            messages.error(request, 'El nombre de la categoría es requerido.')
            return redirect('inventory_manage')

        try:
            catalog = self.get_catalog()
            if Category.objects.filter(catalog=catalog, name=name).exists():
                messages.error(request, 'Ya existe una categoría con este nombre.')
            else:
                category = Category.objects.create(name=name, catalog=catalog)
                messages.success(request, f'Categoría «{category.name}» creada con éxito.')
        except Exception as e:
            messages.error(request, f'Error al crear categoría: {str(e)}')

        return redirect('inventory_manage')


class EditCategoryView(CategoryBaseView):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        new_name = request.POST.get('nombre', '').strip()
        if not new_name:
            messages.error(request, 'El nombre de la categoría es requerido.')
            return redirect('inventory_manage')

        try:
            if Category.objects.filter(catalog=category.catalog, name=new_name).exclude(id=category.id).exists():
                messages.error(request, 'Ya existe una categoría con este nombre.')
            else:
                category.name = new_name
                category.save()
                messages.success(request, f'Categoría «{category.name}» actualizada con éxito.')
        except Exception as e:
            messages.error(request, f'Error al editar categoría: {str(e)}')

        return redirect('inventory_manage')


class DeleteCategoryView(CategoryBaseView):
    def post(self, request, pk):
        try:
            category = get_object_or_404(Category, pk=pk)
            name = category.name
            category.delete()
            messages.success(request, f'Categoría «{name}» eliminada con éxito.')
        except Exception as e:
            messages.error(request, f'Error al eliminar categoría: {str(e)}')

        return redirect('inventory_manage')


def _safe_float(value, default=0.0):
    """Convierte un valor a float de forma segura, manejando comas como separadores decimales."""
    if value is None:
        return default
    try:
        # Reemplaza coma por punto para locales que usan coma decimal
        return float(str(value).replace(',', '.').strip() or default)
    except (ValueError, TypeError):
        return default


def _safe_int(value, default=0):
    """Convierte un valor a int de forma segura."""
    if value is None:
        return default
    try:
        return int(str(value).strip() or default)
    except (ValueError, TypeError):
        return default


class ManageInventoryView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'DESIGN']

    def get(self, request):
        category_filter = request.GET.get('filter_cat', '')

        categories = Category.objects.all().order_by('name')
        catalogs = Catalog.objects.all().order_by('name')
        products = Product.objects.all().order_by('-id')

        if category_filter:
            products = products.filter(category__id=category_filter)

        context = {
            'categories': categories,
            'catalogs': catalogs,
            'products': products,
            'category_filter': category_filter,
        }
        return render(request, 'inventory/productos.html', context)

    def post(self, request):
        action = request.POST.get('action', '').strip()

        # ── Agregar producto (form normal) ─────────────────────────────────
        if action == 'add':
            try:
                name = request.POST.get('nombre', '').strip()
                desc = request.POST.get('descripcion', '')
                category_id = request.POST.get('categoria')
                price = _safe_float(request.POST.get('precio', '0'))
                cost = _safe_float(request.POST.get('costo', '0'))
                stock = _safe_int(request.POST.get('stock', '0'))
                featured = request.POST.get('destacado') == 'on'

                if not name:
                    messages.error(request, "El nombre de la prenda es obligatorio.")
                    return redirect('inventory_manage')

                category = Category.objects.filter(id=category_id).first()
                catalog = category.catalog if category else None

                product = Product.objects.create(
                    name=name, description=desc, catalog=catalog, category=category,
                    price=price, cost=cost, stock=stock, featured=featured
                )
                if 'imagen' in request.FILES:
                    product.image = request.FILES['imagen']
                    product.save()

                # Agregar movimiento inicial a Kardex si hay stock inicial
                if stock > 0:
                    Kardex.objects.create(
                        product=product,
                        movement_type='Entrada',
                        quantity=stock,
                        prev_stock=0,
                        new_stock=stock,
                        reason='Stock inicial al crear producto',
                        user=request.user
                    )

                messages.success(request, f"Prenda «{product.name}» agregada con éxito.")

            except Exception as e:
                messages.error(request, f"Error al agregar prenda: {str(e)}")

            return redirect('inventory_manage')

        # ── Crear categoría ─────────────────────────────────────────
        elif action in {'create_category', 'create'}:
            return CreateCategoryView.as_view()(request)

        # ── Editar categoría ────────────────────────────────────────
        elif action in {'edit_category', 'edit'}:
            category_id = request.POST.get('id') or request.POST.get('category_id')
            if category_id:
                return EditCategoryView.as_view()(request, pk=category_id)
            messages.error(request, 'No se encontró la categoría a editar.')
            return redirect('inventory_manage')

        # ── Eliminar categoría ──────────────────────────────────────
        elif action in {'delete_category', 'delete'}:
            category_id = request.POST.get('id') or request.POST.get('category_id')
            if category_id:
                return DeleteCategoryView.as_view()(request, pk=category_id)
            messages.error(request, 'No se encontró la categoría a eliminar.')
            return redirect('inventory_manage')

        return redirect('inventory_manage')


class EditProductView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'DESIGN']

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        categories = Category.objects.all().order_by('name')
        context = {
            'product': product,
            'categories': categories,
        }
        return render(request, 'inventory/product_edit.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        try:
            name = request.POST.get('nombre', '').strip()
            if not name:
                messages.error(request, "El nombre del producto es obligatorio.")
                return redirect('product_edit', pk=pk)

            desc = request.POST.get('descripcion', '')
            category_id = request.POST.get('categoria')
            price = _safe_float(request.POST.get('precio', '0'))
            cost = _safe_float(request.POST.get('costo', '0'))
            stock = _safe_int(request.POST.get('stock', '0'))
            featured = request.POST.get('destacado') == 'on'

            category = Category.objects.filter(id=category_id).first()
            catalog = category.catalog if category else None

            prev_stock = product.stock

            product.name = name
            product.description = desc
            product.catalog = catalog
            product.category = category
            product.price = price
            product.cost = cost
            product.stock = stock
            product.featured = featured

            if 'imagen' in request.FILES:
                product.image = request.FILES['imagen']
            product.save()

            # Registrar en kardex si cambió el stock
            if prev_stock != stock:
                mov_type = 'Entrada' if stock > prev_stock else 'Salida'
                diff = abs(stock - prev_stock)
                Kardex.objects.create(
                    product=product,
                    movement_type=mov_type,
                    quantity=diff,
                    prev_stock=prev_stock,
                    new_stock=stock,
                    reason='Ajuste Manual - Edición Externa',
                    user=request.user
                )

            messages.success(request, f"Producto «{product.name}» actualizado correctamente.")
            return redirect('inventory_manage')

        except Exception as e:
            messages.error(request, f"Error al actualizar producto: {str(e)}")
            return redirect('product_edit', pk=pk)


class DeleteProductView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'DESIGN']

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        name = product.name
        try:
            product.delete()
            messages.success(request, f"Producto «{name}» eliminado con éxito.")
        except Exception as e:
            messages.error(request, f"Error al eliminar producto: {str(e)}")
        return redirect('inventory_manage')
