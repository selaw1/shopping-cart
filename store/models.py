"""
Django models for store app

contains an order model related by one to many relationship with a product model
"""
from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=255)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    quantity_in_stock = models.PositiveIntegerField()
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="product_order",
    )

    def __str__(self):
        return self.name
