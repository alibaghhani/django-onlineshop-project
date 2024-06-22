from config.settings import ORDER_SESSION_ID
from product.models import Product


class Cart:
    """

    cart class for creating, adding, deleting, object to cart
    using sessions so users can add items to their carts without
    login or creat account

    """

    def __init__(self, request):
        self.session = request.session
        order = self.session.get(ORDER_SESSION_ID)
        if not order:
            order = self.session[ORDER_SESSION_ID] = {}
        self.order = order

    def __iter__(self):
        ids = self.order.keys()
        products = Product.objects.filter(id__in=ids)
        order = self.order.copy()
        for product in products:
            if str(product.id) in order:
                order[str(product.id)]['product'] = product
        for value in order.values():
            if 'price' in value and 'quantity' in value:
                value['total_price'] = int(value.get("price", 0)) * value.get("quantity", 0)
                yield value

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.order:
            self.order[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.order[product_id]['quantity'] += quantity
        self.save_session()

    def __len__(self):
        return sum(value['quantity'] for value in self.order.values())

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.order:
            del self.order[product_id]
        self.save_session()

    def save_session(self):
        self.session.modified = True

    def get_final_price(self):
        return sum(value['product'].price * value['quantity'] for value in self.order.values())

    def decrease_quantity(self, product_id, quantity):
        if product_id in self.order:
            self.order[product_id]['quantity'] = quantity
            self.save_session()
            return self.order
        else:
            raise RuntimeError('object does not exists')

    def delete(self):
        self.session[ORDER_SESSION_ID] = {}
        self.save_session()
