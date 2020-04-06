from django import forms


QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 20)]


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(label='Количество',
                                  required=True,
                                  initial=1,
                                  min_value=1)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
