from django.contrib import admin

from .models import (Item, OrderItem, Order)

# Item
admin.site.register(Item)

# Order Item
admin.site.register(OrderItem)

# Order
admin.site.register(Order)
