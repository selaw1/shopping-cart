from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import F
from django.db.models import Sum

from .models import Product



def shopping_cart(request):
    products = Product.objects.filter(in_stock=True)
    total_price = Product.objects.aggregate(Sum('price'))['price__sum']


    if request.method == 'POST':
        names = request.POST.getlist('name')
        quantity = request.POST.getlist('quantity')

        for n,q in zip(names, quantity):
            product = Product.objects.get(name=n)

            if product.quantity_in_stock == 0:
                product.in_stock = False
                product.save()
                messages.add_message(
                    request,
                    messages.ERROR,
                    f'I\'m sorry but we are out of stock for {n}'
                ) 
                return redirect('/')

            if int(q) > product.quantity_in_stock:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f'I\'m sorry but we only have {product.quantity_in_stock}kg of {n} left'
                ) 
                return redirect('/')

            product.quantity_in_stock = F('quantity_in_stock') - int(q)
            product.save()

        messages.add_message(
            request,
            messages.SUCCESS,
            'We recieved your order successfully'
        ) 
        return redirect('/')
    return render(request, 'cart.html', {'products':products, 'total_price':total_price})