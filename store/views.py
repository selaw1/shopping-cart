"""
Django views for store app

contains a generic form class for displaying all products in an order object as an editable form
"""
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import F
from django.db.models import Sum

from .models import Product, Order
from .forms import ProductFormSet


class ShoppingCartEditView(SingleObjectMixin, FormView):
    model = Order
    template_name = "cart.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Order.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Order.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        return ProductFormSet(**self.get_form_kwargs(), instance=self.object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = self.object.product_order.all()
        if products:
            total_price = self.update_total_price()
        else:
            total_price = self.object.total_price

        context["total_price"] = total_price
        return context

    def form_valid(self, form):
        if "buy" in self.request.POST:
            products = self.object.product_order.all()
            self.reset_quantity(products)

            total_price = self.object.total_price
            self.update_total_price()

            messages.add_message(
                self.request,
                messages.SUCCESS,
                f"We recieved your order successfully, you spent ${total_price}",
            )
        elif "validate" in self.request.POST:
            form.save()
            total_price = self.update_total_price()

            messages.add_message(
                self.request,
                messages.SUCCESS,
                f"Products are available, total price is ${total_price}",
            )

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("store:order_details", kwargs={"pk": self.object.pk})

    def update_total_price(self):
        total_price = self.object.product_order.all().aggregate(
            total_price=Sum(F("price") * F("quantity"))
        )["total_price"]
        self.object.total_price = total_price
        self.object.save()
        return total_price

    def reset_quantity(self, products):
        default_value = Product._meta.get_field("quantity").get_default()
        for product in products:
            product.quantity_in_stock = F("quantity_in_stock") - F("quantity")
            product.quantity = default_value
            product.save()
