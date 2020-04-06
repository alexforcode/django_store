from django import forms

from orders.models import Order


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta():
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address']
