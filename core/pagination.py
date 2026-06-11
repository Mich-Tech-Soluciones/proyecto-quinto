"""
Paginadores personalizados para el proyecto
"""

from django.core.paginator import Paginator, Page
from django.utils.functional import cached_property


class CustomPageMixin:
    """
    Mixin personalizado para páginas
    """
    
    @cached_property
    def paginator(self):
        return Paginator(self.object_list, self.paginate_by)
    
    def get_page(self):
        paginator = self.paginator
        page_number = self.request.GET.get('page', 1)
        
        try:
            page = int(page_number)
        except ValueError:
            page = 1
        
        return paginator.get_page(page)


class CustomPaginator(Paginator):
    """
    Paginador personalizado con configuración adicional
    """
    
    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        super().__init__(object_list, per_page, orphans, allow_empty_first_page)
        self.orphans = orphans


def get_page_context(queryset, request, page_size=20):
    """
    Obtiene contexto de paginación
    
    Args:
        queryset: QuerySet a paginar
        request: HttpRequest
        page_size: Número de items por página
    
    Returns:
        dict: Contexto con información de paginación
    """
    paginator = Paginator(queryset, page_size)
    page_number = request.GET.get('page', 1)
    
    try:
        page = int(page_number)
    except ValueError:
        page = 1
    
    page_obj = paginator.get_page(page)
    
    return {
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'total_items': paginator.count,
        'items_per_page': page_size,
    }
