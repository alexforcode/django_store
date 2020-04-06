from celery import task
from django.core.mail import send_mail
from django.conf import settings

from orders.models import Order


@task
def order_created_mail(order_id):
    '''
    Отправляет письмо с заказом на email из заказа.
    Возвращает 1 (успешно отправлено) или 0 (не отправлено).
    '''
    order = Order.objects.get(id=order_id)
    subject = f'Магазин. Заказ №{order.id}'
    message = f'Заказ успешно добавлен на имя: {order.first_name} {order.last_name}.\n \
                Номер вашего заказа: {order.id}'
    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])

    return mail_sent
