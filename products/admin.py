from django.contrib import admin
from . import models


# Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')


admin.site.register(models.Product, ProductAdmin)


# Offer
class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount')


admin.site.register(models.Offer, OfferAdmin)
