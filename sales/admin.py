from django.contrib import admin
from .models import Order, OrderDetail, Payment


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 0
    readonly_fields = ('unit_price', 'unit_cost', 'subtotal')


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('date',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'company', 'total', 'payment_status', 'status', 'created_at', 'user')
    search_fields = ('customer_name', 'customer_email', 'company', 'id')
    list_filter = ('payment_status', 'status', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [OrderDetailInline, PaymentInline]


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price', 'unit_cost', 'subtotal')
    search_fields = ('order__id', 'product__name')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'note', 'date', 'user')
    search_fields = ('order__id', 'note')
    list_filter = ('payment_method', 'date')
