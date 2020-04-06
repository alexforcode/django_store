from django.test import TestCase

from main.models import Category, Product, get_image_path
from orders.models import Order, OrderItem


CATEGORY_TITLE = 'Категория'
CATEGORY_SLUG = 'kategorija'
PRODUCT_TITLE = 'Продукт'
PRODUCT_SLUG = 'produkt'
PRODUCT_PRICE = 1500.00
IMAGE = 'produkt.jpg'
ORDER_FIRST_NAME = 'Иван'
ORDER_LAST_NAME = 'Иванов'
ORDER_EMAIL = 'ivan@example.com'
ORDER_ADDRESS = 'г.Москва, Кремль, д.1'


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(title=CATEGORY_TITLE, slug=CATEGORY_SLUG)

    def test_title_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_slug_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('slug').max_length
        self.assertEquals(max_length, 100)

    def test_slug_unique(self):
        category = Category.objects.get(id=1)
        unique = category._meta.get_field('slug').unique
        self.assertTrue(unique)

    def test_object_name_is_title(self):
        category = Category.objects.get(id=1)
        self.assertEquals(f'{category.title}', str(category))

    def test_get_absolute_url(self):
        category = Category.objects.get(id=1)
        self.assertEquals(category.get_absolute_url(), f'/category/{category.slug}')


class ProductModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title=CATEGORY_TITLE, slug=CATEGORY_SLUG)
        cat_id = category.id
        Product.objects.create(title=PRODUCT_TITLE,
                               slug=PRODUCT_SLUG,
                               price=PRODUCT_PRICE,
                               category_id=cat_id)

    def test_title_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('title').max_length
        self.assertEquals(max_length, 150)

    def test_slug_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('slug').max_length
        self.assertEquals(max_length, 150)

    def test_slug_unique(self):
        product = Product.objects.get(id=1)
        unique = product._meta.get_field('slug').unique
        self.assertTrue(unique)

    def test_price(self):
        product = Product.objects.get(id=1)
        price_str = product.price.to_eng_string()
        self.assertEquals(price_str, str(product.price))

    def test_image_path(self):
        product = Product.objects.get(id=1)
        image_path = get_image_path(product, IMAGE)
        self.assertEquals(image_path, f'products/{product.slug}/{IMAGE}')

    def test_default_available(self):
        product = Product.objects.get(id=1)
        self.assertTrue(product.available)

    def test_object_name_is_title(self):
        product = Product.objects.get(id=1)
        self.assertEquals(f'{product.title}', str(product))

    def test_get_absolute_url(self):
        product = Product.objects.get(id=1)
        self.assertEquals(product.get_absolute_url(), f'/product/{product.slug}')


class OrderModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        Order.objects.create(first_name=ORDER_FIRST_NAME,
                             last_name=ORDER_LAST_NAME,
                             email=ORDER_EMAIL,
                             address=ORDER_ADDRESS)

    def test_first_name_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 50)

    def test_address_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('address').max_length
        self.assertEquals(max_length, 250)

    def test_default_paid(self):
        order = Order.objects.get(id=1)
        self.assertFalse(order.paid)

    def test_object_name_is_str_with_id(self):
        order = Order.objects.get(id=1)
        self.assertEquals(f'Заказ {order.id}', str(order))


class OrderItemModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(title=CATEGORY_TITLE, slug=CATEGORY_SLUG)
        cat_id = category.id
        for prod_num in range(1, 4):
            product = Product.objects.create(title=f'{PRODUCT_TITLE} {prod_num}',
                                             slug=f'{PRODUCT_SLUG}-{prod_num}',
                                             price=PRODUCT_PRICE,
                                             category_id=cat_id)
        order = Order.objects.create(first_name=ORDER_FIRST_NAME,
                                     last_name=ORDER_LAST_NAME,
                                     email=ORDER_EMAIL,
                                     address=ORDER_ADDRESS)
        for product in Product.objects.all():
            OrderItem.objects.create(order=order,
                                     product=product,
                                     price=product.price)

    def test_default_quantity(self):
        order_item = OrderItem.objects.get(id=1)
        self.assertEquals(1, order_item.quantity)

    def test_object_name_is_str_with_id(self):
        order_item = OrderItem.objects.get(id=1)
        self.assertEquals(f'{order_item.id}', str(order_item))

    def test_order_item_cost(self):
        order_item = OrderItem.objects.get(id=1)
        self.assertEquals(order_item.price * order_item.quantity, order_item.get_cost())

    def test_order_total_cost(self):
        order = Order.objects.get(id=1)
        self.assertEquals(order.get_total_cost(), 4500.00)
