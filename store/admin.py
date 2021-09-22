"""
Django admin for store app

displays the models on the django admin page
"""
from django.contrib import admin

from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "order",
        "price",
        "quantity",
        "quantity_in_stock",
    ]
    list_filter = ["name", "order"]
    list_editable = [
        "price",
        "quantity",
        "quantity_in_stock",
    ]

    fieldsets = (
        (
            "Product Info",
            {
                "fields": (
                    "name",
                    "order",
                    "quantity",
                    "price",
                    "quantity_in_stock",
                )
            },
        ),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["name", "total_price", "id"]
    list_filter = ["name"]

    fieldsets = (("Product Info", {"fields": ("name", "total_price")}),)
