from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from cart.forms import CartAddProductForm
from main.models import Category, Product


def get_paginator(request, object_list, per_page=10):
    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    prev_url = f'?page={page.previous_page_number()}' if page.has_previous() else ''
    next_url = f'?page={page.next_page_number()}' if page.has_next() else ''

    context = {
        'content_objects': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url
    }

    return context


def shop_view(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'cart_product_form': cart_product_form,
        'categories': categories,
    }
    paginator_context = get_paginator(request, products, 6)
    context.update(paginator_context)

    return render(request, 'main/shop.html', context)


def product_view(request, product_slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, slug=product_slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'cart_product_form': cart_product_form,
        'categories': categories,
        'product': product,
    }

    return render(request, 'main/product.html', context)


def category_view(request, category_slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(available=True).filter(category=category)
    cart_product_form = CartAddProductForm()
    context = {
        'cart_product_form': cart_product_form,
        'categories': categories,
        'category': category,
    }
    paginator_context = get_paginator(request, products, 6)
    context.update(paginator_context)

    return render(request, 'main/shop.html', context)


def search_view(request):
    products = Product.objects.all()
    query = request.GET.get('q')
    founded = []
    # т.к. SQLite не поддерживает регистронезависимый поиск Unicode,
    # поэтому нельзя использовать __icontains
    for product in products:
        if query.lower() in product.title.lower():
            founded.append(product)

    categories = Category.objects.all()
    cart_product_form = CartAddProductForm()

    context = {
        'cart_product_form': cart_product_form,
        'categories': categories,
        'founded': founded
    }

    return render(request, 'main/search.html', context)
