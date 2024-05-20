from django import forms

class CartItemQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1,max_value=15)