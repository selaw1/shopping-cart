"""
Django forms for store app

contains an inline formset to generate a form for all products in an order object and validate the input data
"""
from django import forms
from django.contrib.messages.api import error
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory

from .models import Product, Order


OrderProductFormSet = inlineformset_factory(
    Order,
    Product,
    fields=(
        "name",
        "quantity",
        "price",
    ),
    extra=0,
    can_delete=False,
)


class ProductFormSet(OrderProductFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields["name"].label = ""
        form.fields["quantity"].label = ""
        form.fields["price"].label = ""
        form.fields["name"].widget.attrs.update({"readonly": "readonly"})
        form.fields["price"].widget.attrs.update({"readonly": "readonly"})

    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data

        if "validate" in self.data:
            for data in cleaned_data:
                product = Product.objects.get(name=data["name"])

                if product.quantity_in_stock == 0:
                    product.in_stock = False
                    product.save()
                    raise forms.ValidationError(
                        f'I\'m sorry but we are out of stock for {data["name"]}'
                    )

                if data["quantity"] > product.quantity_in_stock:
                    raise forms.ValidationError(
                        f'I\'m sorry but we only have {product.quantity_in_stock}kg of {data["name"]} left'
                    )
