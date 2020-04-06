from django.urls import path

from orders import views


app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create_view, name='order_create'),
]
