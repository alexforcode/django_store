from django.urls import path

from main import views


app_name = 'main'

urlpatterns = [
    path('', views.shop_view, name='shop'),
    path('category/<str:category_slug>', views.category_view, name='category'),
    path('product/<str:product_slug>', views.product_view, name='product'),
    path('search/', views.search_view, name='search'),
]
