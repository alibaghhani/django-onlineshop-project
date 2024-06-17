from django import forms


# quantity form for choose quantity for items to add to cart
class CartItemQuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1,max_value=15)