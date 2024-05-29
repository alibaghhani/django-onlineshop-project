from django.contrib.auth import get_user_model
from .cart import Cart
user_ = get_user_model
def order(request):
    return {'order': Cart(request)}

def user(request):
    return {'user':user_}