from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price', 'quantity_in_stock', 'in_stock']
    list_filter = ['in_stock', 'name']
    list_editable = ['price', 'quantity_in_stock']

    fieldsets = (
        ('Product Info', {"fields": ('name', 'price', 'quantity_in_stock', 'in_stock')}),
        )

