from django.contrib.auth import get_user_model

from .cart import Cart

user_ = get_user_model


# context processor for using model below in all over templates
def order(request):
    return {'order': Cart(request)}


def user():
    return {'user': user_}
