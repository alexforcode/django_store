from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory
from django.conf import settings

from main.models import Product, Category
from orders.models import Order
from cart.cart import Cart
from orders.tasks import order_created_mail


CATEGORY_TITLE = 'Категория'
CATEGORY_SLUG = 'kategorija'
PRODUCT_TITLE = 'Продукт'
PRODUCT_SLUG = 'produkt'
PRODUCT_PRICE = 100.00
FIRST_NAME = 'Иван'
LAST_NAME = 'Иванов'
EMAIL = 'alexgir@inbox.ru'
ADDRESS = 'г.Москва, Кремль, д.1'


class CartModuleTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title=CATEGORY_TITLE, slug=CATEGORY_SLUG)
        cat_id = category.id
        for prod_num in range(1, 5):
            Product.objects.create(title=f'{PRODUCT_TITLE} {prod_num}',
                                   slug=f'{PRODUCT_SLUG}-{prod_num}',
                                   price=PRODUCT_PRICE * prod_num,
                                   category_id=cat_id)

    def setUp(self):
        self.request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

    def test_initialize_cart_clean_session(self):
        request = self.request
        Cart(request)
        self.assertEqual(request.session[settings.CART_SESSION_ID], {})

    def test_remove_cart_from_session(self):
        request = self.request
        cart = Cart(request)
        self.assertTrue(settings.CART_SESSION_ID in request.session.keys())
        cart.clear()
        self.assertFalse(settings.CART_SESSION_ID in request.session.keys())

    def test_add_to_cart(self):
        request = self.request
        cart = Cart(request)
        product = Product.objects.get(id=1)
        cart.add(product)
        self.assertEqual(len(cart), 1)

    def test_update_product_quantity(self):
        request = self.request
        cart = Cart(request)
        product = Product.objects.get(id=1)
        cart.add(product)
        self.assertEqual(len(cart), 1)
        cart.add(product=product, quantity=5, update=True)
        self.assertEqual(cart.cart['1']['quantity'], 5)

    def test_remove_from_cart(self):
        request = self.request
        cart = Cart(request)
        product = Product.objects.get(id=1)
        cart.add(product)
        self.assertEqual(len(cart), 1)
        cart.remove(product)
        self.assertEqual(len(cart), 0)

    def test_get_total_price_in_cart(self):
        request = self.request
        cart = Cart(request)
        for prod_id in range(1, 5):
            product = Product.objects.get(id=prod_id)
            cart.add(product)
        self.assertEqual(cart.get_total_price(), 1000.00)

    def test_cart_iteration(self):
        request = self.request
        cart = Cart(request)
        for prod_id in range(1, 5):
            product = Product.objects.get(id=prod_id)
            cart.add(product)
        for item in cart:
            self.assertTrue(item)
            return
        self.assertFalse(True)


class TasksModuleTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Order.objects.create(first_name=FIRST_NAME,
                             last_name=LAST_NAME,
                             email=EMAIL,
                             address=ADDRESS)

    def test_sending_mail_with_order_id(self):
        sent = order_created_mail(order_id=1)
        self.assertEqual(sent, 1)
