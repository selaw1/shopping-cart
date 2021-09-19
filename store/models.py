from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    quantity_in_stock = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name
