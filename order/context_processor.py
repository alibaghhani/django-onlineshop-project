from .order import Order

def cart(request):
    return {'order': Order(request)}