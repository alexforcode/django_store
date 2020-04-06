from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory

from cart.forms import CartAddProductForm
from orders.forms import OrderCreateForm
from users.forms import UserRegistrationForm, UserLoginForm


FIRST_NAME = 'Иван'
LAST_NAME = 'Иванов'
EMAIL = 'ivan@example.com'
ADDRESS = 'г.Москва, Кремль, д.1'
USERNAME = 'ivan'
PASSWORD = 'susanin2019'


class CartAddProductFormTest(TestCase):

    def test_quantity_field_label(self):
        form = CartAddProductForm()
        self.assertTrue(form.fields['quantity'].label == 'Количество')

    def test_quantity_positive(self):
        form_data = {'quantity': 10}
        form = CartAddProductForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_quantity_negative(self):
        form_data = {'quantity': -10}
        form = CartAddProductForm(data=form_data)
        self.assertFalse(form.is_valid())


class OrderCreateFormTest(TestCase):

    def test_first_name_field_label(self):
        form = OrderCreateForm()
        self.assertTrue(form.fields['first_name'].label == 'Имя')

    def test_last_name_field_label(self):
        form = OrderCreateForm()
        self.assertTrue(form.fields['last_name'].label == 'Фамилия')

    def test_email_field_label(self):
        form = OrderCreateForm()
        self.assertTrue(form.fields['email'].label == 'Email')

    def test_address_field_label(self):
        form = OrderCreateForm()
        self.assertTrue(form.fields['address'].label == 'Адрес')

    def test_form_is_valid(self):
        form_data = {'first_name': FIRST_NAME,
                     'last_name': LAST_NAME,
                     'email': EMAIL,
                     'address': ADDRESS}
        form = OrderCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_first_name_field(self):
        form_data = {'first_name': '',
                     'last_name': LAST_NAME,
                     'email': EMAIL,
                     'address': ADDRESS}
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_last_name_field(self):
        form_data = {'first_name': FIRST_NAME,
                     'last_name': '',
                     'email': EMAIL,
                     'address': ADDRESS}
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_email_field(self):
        form_data = {'first_name': FIRST_NAME,
                     'last_name': LAST_NAME,
                     'email': 'ivan',
                     'address': ADDRESS}
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_address_field(self):
        form_data = {'first_name': FIRST_NAME,
                     'last_name': LAST_NAME,
                     'email': EMAIL,
                     'address': ''}
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserRegistrationFormTest(TestCase):

    def test_form_is_valid(self):
        form_data = {'username': USERNAME,
                     'email': EMAIL,
                     'password': PASSWORD,
                     'password_confirm': PASSWORD}
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_username_field(self):
        form_data = {'username': '',
                     'email': EMAIL,
                     'password': PASSWORD,
                     'password_confirm': PASSWORD}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_email_field(self):
        form_data = {'username': USERNAME,
                     'email': 'ivan',
                     'password': PASSWORD,
                     'password_confirm': PASSWORD}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_password_field(self):
        form_data = {'username': USERNAME,
                     'email': EMAIL,
                     'password': 'qwerty',
                     'password_confirm': PASSWORD}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_password_confirm_field(self):
        form_data = {'username': USERNAME,
                     'email': EMAIL,
                     'password': PASSWORD,
                     'password_confirm': 'qwerty'}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserLoginFormTest(TestCase):

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

    def test_form_is_valid(self):
        form_data = {'username': USERNAME,
                     'password': PASSWORD}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_username_field(self):
        form_data = {'username': 'petya',
                     'password': PASSWORD}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_password_field(self):
        form_data = {'username': USERNAME,
                     'password': '12345'}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
