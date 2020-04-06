from django.urls import reverse
from rest_framework.test import APITestCase

from main.models import Product, Category


CATEGORY_TITLE = 'Категория'
CATEGORY_SLUG = 'kategorija'
PRODUCT_TITLE = 'Продукт'
PRODUCT_SLUG = 'produkt'
PRODUCT_PRICE = 100.00


class APIViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        for cat_num in range(1, 4):
            Category.objects.create(title=f'{CATEGORY_TITLE} {cat_num}',
                                    slug=f'{CATEGORY_SLUG}-{cat_num}')
        for prod_num in range(1, 5):
            Product.objects.create(title=f'{PRODUCT_TITLE} {prod_num}',
                                   slug=f'{PRODUCT_SLUG}-{prod_num}',
                                   price=PRODUCT_PRICE * prod_num,
                                   category_id=1)

    def test_categories_view_url_exists(self):
        resp = self.client.get(f'/api/categories/')
        self.assertEqual(resp.status_code, 200)

    def test_categories_view_url_access_by_name(self):
        resp = self.client.get(reverse('api:category_list'))
        self.assertEqual(resp.status_code, 200)

    def test_categories_data(self):
        resp = self.client.get(reverse('api:category_list'))
        self.assertEqual(len(resp.data), 3)

    def test_products_view_url_exists(self):
        resp = self.client.get(f'/api/products/')
        self.assertEqual(resp.status_code, 200)

    def test_products_view_url_access_by_name(self):
        resp = self.client.get(reverse('api:product_list'))
        self.assertEqual(resp.status_code, 200)

    def test_products_data(self):
        resp = self.client.get(reverse('api:product_list'))
        self.assertEqual(len(resp.data), 4)

    def test_product_detail_view_url_exists(self):
        resp = self.client.get(f'/api/products/1/')
        self.assertEqual(resp.status_code, 200)

    def test_product_detail_view_url_access_by_name(self):
        resp = self.client.get(reverse('api:product_detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_product_detail_data(self):
        resp = self.client.get(reverse('api:product_detail', kwargs={'pk': 1}))
        self.assertEqual(resp.data['title'], 'Продукт 1')
