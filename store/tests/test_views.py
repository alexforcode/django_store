from random import choice

from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.urls import reverse

from main.models import Product, Category


CATEGORY_TITLE = 'Категория'
CATEGORY_SLUG = 'kategorija'
PRODUCT_TITLE = 'Продукт'
PRODUCT_SLUG = 'produkt'
PRODUCT_PRICE = 100.00
USERNAME = 'ivan'
NEW_USERNAME = 'petr'
PASSWORD = 'susanin2019'
NEW_PASSWORD = 'perviy2019'
EMAIL = 'ivan@example.com'
NEW_EMAIL = 'petr@example.com'


class ShopViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title=CATEGORY_TITLE, slug=CATEGORY_SLUG)
        cat_id = category.id
        for prod_num in range(1, 10):
            Product.objects.create(title=f'{PRODUCT_TITLE} {prod_num}',
                                   slug=f'{PRODUCT_SLUG}-{prod_num}',
                                   price=PRODUCT_PRICE * prod_num,
                                   category_id=cat_id)

    def test_view_url_exists(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_access_by_name(self):
        resp = self.client.get(reverse('main:shop'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('main:shop'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main/shop.html')

    def test_pagination_on_first_page(self):
        resp = self.client.get(reverse('main:shop'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['content_objects']) == 6)

    def test_pagination_on_second_page(self):
        resp = self.client.get(f"{reverse('main:shop')}?page=2")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertTrue(len(resp.context['content_objects']) == 3)


class ProductViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title=CATEGORY_TITLE, slug=CATEGORY_SLUG)
        cat_id = category.id
        Product.objects.create(title=PRODUCT_TITLE,
                               slug=PRODUCT_SLUG,
                               price=PRODUCT_PRICE,
                               category_id=cat_id)

    def test_view_url_exists(self):
        resp = self.client.get(f'/product/{PRODUCT_SLUG}')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_access_by_name(self):
        resp = self.client.get(reverse('main:product', kwargs={'product_slug': PRODUCT_SLUG}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('main:product', kwargs={'product_slug': PRODUCT_SLUG}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main/product.html')


class CategoryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cat_ids = list()
        for cat_num in range(1, 4):
            category = Category.objects.create(title=f'{CATEGORY_TITLE} {cat_num}',
                                               slug=f'{CATEGORY_SLUG}-{cat_num}')
            cat_ids.append(category.id)
        for prod_num in range(1, 20):
            Product.objects.create(title=f'{PRODUCT_TITLE} {prod_num}',
                                   slug=f'{PRODUCT_SLUG}-{prod_num}',
                                   price=PRODUCT_PRICE * prod_num,
                                   category_id=choice(cat_ids))

    def test_view_url_exists(self):
        for cat_num in range(1, 4):
            resp = self.client.get(f'/category/{CATEGORY_SLUG}-{cat_num}')
            self.assertEqual(resp.status_code, 200)

    def test_view_url_access_by_name(self):
        for cat_num in range(1, 4):
            resp = self.client.get(reverse('main:category', kwargs={'category_slug': f'{CATEGORY_SLUG}-{cat_num}'}))
            self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('main:category', kwargs={'category_slug': f'{CATEGORY_SLUG}-1'}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'main/shop.html')


class SearchViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title=CATEGORY_TITLE, slug=CATEGORY_SLUG)
        cat_id = category.id
        for prod_num in range(1, 10):
            Product.objects.create(title=f'{PRODUCT_TITLE} {prod_num}',
                                   slug=f'{PRODUCT_SLUG}-{prod_num}',
                                   price=PRODUCT_PRICE * prod_num,
                                   category_id=cat_id)

    def test_view_url_exists(self):
        resp = self.client.get('/search/?q=Продукт')
        self.assertEqual(resp.status_code, 200)


class CartViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title=CATEGORY_TITLE, slug=CATEGORY_SLUG)
        cat_id = category.id
        Product.objects.create(title=PRODUCT_TITLE,
                               slug=PRODUCT_SLUG,
                               price=PRODUCT_PRICE,
                               category_id=cat_id)

    def setUp(self):
        self.request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

    def test_view_url_exists(self):
        resp = self.client.get('/cart/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_access_by_name(self):
        resp = self.client.get(reverse('cart:cart'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('cart:cart'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cart/cart.html')

    def test_view_add_to_cart(self):
        resp = self.client.post(reverse('cart:cart_add'), {'product_id': 1})
        self.assertEqual(resp.status_code, 200)

    def test_view_update_product_in_cart(self):
        self.client.post(reverse('cart:cart_add'), {'product_id': 1})
        resp = self.client.post('/cart/update/1', {'quantity': 2, 'update': True})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], reverse('cart:cart'))

    def test_view_remove_from_cart(self):
        self.client.post(reverse('cart:cart_add'), {'product_id': 1})
        resp = self.client.get('/cart/remove/1')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], reverse('cart:cart'))


class OrderViewTest(TestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

    def test_view_url_exists(self):
        resp = self.client.get('/orders/create/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_access_by_name(self):
        resp = self.client.get(reverse('orders:order_create'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('orders:order_create'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'orders/order_create.html')


class UsersViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username=USERNAME)
        user.set_password(PASSWORD)
        user.save()

    def setUp(self):
        self.request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

    def test_register_view_url_exist(self):
        resp = self.client.get('/users/register/')
        self.assertEqual(resp.status_code, 200)

    def test_register_view_url_access_by_name(self):
        resp = self.client.get(reverse('users:register'))
        self.assertEqual(resp.status_code, 200)

    def test_register_view_uses_correct_template(self):
        resp = self.client.get(reverse('users:register'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/register.html')

    def test_register_view_registration(self):
        context = {
            'username': NEW_USERNAME,
            'email': NEW_EMAIL,
            'password': NEW_PASSWORD,
            'password_confirm': NEW_PASSWORD
        }
        resp = self.client.post(reverse('users:register'), context)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/register_done.html')
        user = User.objects.get(username=NEW_USERNAME)
        self.assertTrue(user)

    def test_login_view_url_exist(self):
        resp = self.client.get('/users/login/')
        self.assertEqual(resp.status_code, 200)

    def test_login_view_url_access_by_name(self):
        resp = self.client.get(reverse('users:login'))
        self.assertEqual(resp.status_code, 200)

    def test_login_view_uses_correct_template(self):
        resp = self.client.get(reverse('users:login'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/login.html')

    def test_login_view_authentication(self):
        user = User.objects.get(username=USERNAME)
        context = {
            'username': USERNAME,
            'password': PASSWORD
        }
        resp = self.client.post(reverse('users:login'), context)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], reverse('main:shop'))
        resp = self.client.get(reverse('main:shop'))
        self.assertEqual(resp.context['user'], user)

    def test_logout_view_url_exist(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        resp = self.client.get('/users/logout/')
        self.assertEqual(resp.status_code, 200)

    def test_logout_view_url_access_by_name(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        resp = self.client.get(reverse('users:logout'))
        self.assertEqual(resp.status_code, 200)

    def test_logout_view_uses_correct_template(self):
        self.client.login(username=USERNAME, password=PASSWORD)
        resp = self.client.get(reverse('users:logout'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/logged_out.html')
