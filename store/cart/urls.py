from django.urls import path

from cart import views


app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/', views.cart_add, name='cart_add'),
    path('update/<int:product_id>', views.cart_update, name='cart_update'),
    path('remove/<int:product_id>', views.cart_remove, name='cart_remove')
]
