from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from main.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm


def cart_view(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    context = {
        'cart': cart
    }

    return render(request, 'cart/cart.html', context)


@require_POST
def cart_add(request):
    cart = Cart(request)
    product = get_object_or_404(Product, id=request.POST.get('product_id'))
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        c_data = form.cleaned_data
        cart.add(product=product,
                 quantity=c_data['quantity'],
                 update=c_data['update'],)

    return JsonResponse({'cart_total': len(cart)})


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        c_data = form.cleaned_data
        cart.add(product=product,
                 quantity=c_data['quantity'],
                 update=c_data['update'],)

    return redirect('cart:cart')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect('cart:cart')
