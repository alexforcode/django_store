from django.shortcuts import render
from kombu.exceptions import OperationalError

from cart.cart import Cart
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from orders.tasks import order_created_mail


def order_create_view(request):
    cart = Cart(request)

    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            # отправка письма на email, используя celery
            try:
                order_created_mail.delay(order.id)
            except OperationalError:
                order_created_mail(order.id)
            context = {
                'order': order,
            }

            return render(request, 'orders/order_thanks.html', context)
    else:
        order_form = OrderCreateForm()

    context = {
        'cart': cart,
        'order_form': order_form,
    }
    return render(request, 'orders/order_create.html', context)
