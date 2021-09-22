"""
Django urls for store app

contains path for the orders
"""
from django.urls import path

from . import views


app_name = "store"
urlpatterns = [
    path("order/<int:pk>", views.ShoppingCartEditView.as_view(), name="order_details")
]
