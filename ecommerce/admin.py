from django.contrib import admin
from .models import *

admin.site.register(Product)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'order_status', 'paid', 'date']


admin.site.register(Order, OrderAdmin)


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = [
        'order_id',
        'product_id',
        'quantity',
        'price',
        'data'
    ]


admin.site.register(OrderDetails, OrderDetailsAdmin)
