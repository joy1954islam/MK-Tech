from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'stock',
        'price',
        'date'
    ]


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'order_status', 'paid', 'total_price', 'date']


admin.site.register(Order, OrderAdmin)


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = [
        'order_id',
        'product_id',
        'quantity',
        'price',
        'is_delivered',
        'date'
    ]


admin.site.register(OrderDetails, OrderDetailsAdmin)
