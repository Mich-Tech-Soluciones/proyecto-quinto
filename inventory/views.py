from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from .models import Product, Catalog, Category, ProductSize, Kardex

class ManageInventoryView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.role in ['ADMIN', 'DESIGN']

    def get(self, request):
        catalog_filter = request.GET.get('filter_catalogo', '')
        category_filter = request.GET.get('filter_cat', '')
        
        catalogs = Catalog.objects.all().order_by('name')
        categories = Category.objects.all().order_by('name')
        
        products = Product.objects.all().order_by('-id')
        if catalog_filter:
            products = products.filter(catalog__name=catalog_filter)
        if category_filter:
            products = products.filter(category__name=category_filter)
            
        edit_product = None
        edit_sizes = []
        if 'edit' in request.GET:
            try:
                edit_product = Product.objects.get(id=request.GET['edit'])
                edit_sizes = edit_product.sizes.all()
            except Product.DoesNotExist:
                pass

        context = {
            'catalogs': catalogs,
            'categories': categories,
            'products': products,
            'catalog_filter': catalog_filter,
            'category_filter': category_filter,
            'edit_product': edit_product,
            'edit_sizes': edit_sizes,
        }
        return render(request, 'inventory/productos.html', context)

    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'update_stock':
            product_id = request.POST.get('id')
            new_stock = int(request.POST.get('stock', 0))
            product = get_object_or_404(Product, id=product_id)
            prev_stock = product.stock
            
            if prev_stock != new_stock:
                mov_type = 'Entrada' if new_stock > prev_stock else 'Salida'
                diff = abs(new_stock - prev_stock)
                product.stock = new_stock
                product.save()
                
                Kardex.objects.create(
                    product=product,
                    movement_type=mov_type,
                    quantity=diff,
                    prev_stock=prev_stock,
                    new_stock=new_stock,
                    reason='Ajuste Manual Rápido',
                    user=request.user
                )
            return JsonResponse({'status': 'OK'})
            
        elif action in ['add', 'edit']:
            product_id = request.POST.get('id')
            name = request.POST.get('nombre')
            desc = request.POST.get('descripcion')
            cat_name = request.POST.get('catalogo')
            subcat_name = request.POST.get('categoria')
            price = request.POST.get('precio', 0)
            cost = request.POST.get('costo', 0)
            stock = request.POST.get('stock', 0)
            featured = request.POST.get('destacado') == 'on'
            
            # Find catalog and category
            catalog = Catalog.objects.filter(name=cat_name).first()
            category = Category.objects.filter(name=subcat_name, catalog=catalog).first()
            
            if action == 'add':
                product = Product.objects.create(
                    name=name, description=desc, catalog=catalog, category=category,
                    price=price, cost=cost, stock=stock, featured=featured
                )
                if 'imagen' in request.FILES:
                    product.image = request.FILES['imagen']
                    product.save()
            else:
                product = get_object_or_404(Product, id=product_id)
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
                
            return redirect('inventory_manage')
            
        elif action == 'add_catalogo':
            name = request.POST.get('nombre_cat')
            icon = request.POST.get('icono_cat', 'bi-folder')
            if name:
                Catalog.objects.get_or_create(name=name, defaults={'icon': icon})
            return redirect('inventory_manage')
            
        elif action == 'add_categoria':
            cat_id = request.POST.get('catalogo_id')
            name = request.POST.get('nombre_sub')
            catalog = get_object_or_404(Catalog, id=cat_id)
            if name:
                Category.objects.get_or_create(catalog=catalog, name=name)
            return redirect('inventory_manage')
            
        return redirect('inventory_manage')
