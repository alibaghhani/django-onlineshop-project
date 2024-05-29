from config.settings import ORDER_SESSION_ID
from product.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        order = self.session.get(ORDER_SESSION_ID)
        if not order:
            order = self.session[ORDER_SESSION_ID] = {}
        self.order = order

    # def __iter__(self):
    #     ids = self.order.keys()
    #     products = Product.objects.filter(id__in=ids)
    #     order = self.order.copy()
    #     for product in products:
    #         order[str(product.id)]['product'] = product
    #     for value in order.values():
    #         value['total_price'] = int(value['price']) * value['quantity']
    #         yield value
    def __iter__(self):
        ids = self.order.keys()
        products = Product.objects.filter(id__in=ids)
        order = self.order.copy()
        for product in products:
            if str(product.id) in order:
                order[str(product.id)]['product'] = product
        for value in order.values():
            if 'price' in value and 'quantity' in value:
                value['total_price'] = int(value['price']) * value['quantity']
                yield value

        # ids = self.order.keys()
        # products = Product.objects.filter(id__in=ids)
        # order = self.order.copy()
        # for product in products:
        #     if str(product.id) in order:
        #         order[str(product.id)]['product'] = product
        # for value in order.values():
        #     if 'product' in value and 'quantity' in value:
        #         product_price = value['product'].price if 'price' in value['product'] else 0
        #         value['total_price'] = int(product_price) * value['quantity']
        #         yield value
        #
        # ids = self.order.keys()
        # products = Product.objects.filter(id__in=ids)
        # order = self.order.copy()
        #
        # for product in products:
        #     product_dict = {
        #         'id': product.id,
        #         'name': product.name,
        #         'price': product.price,
        #     }
        #
        #     if str(product.id) in order:
        #         order[str(product.id)]['product'] = product_dict
        #
        # for value in order.values():
        #     if 'product' in value and 'quantity' in value:
        #         product_price = value['product']['price'] if 'price' in value['product'] else 0
        #         value['total_price'] = int(product_price) * value['quantity']
        #         yield value

    # def add(self, product, quantity):
    #     product_id = str(product.id)
    #     if product_id not in self.order:
    #         self.order[product_id] = {'quantity': 0, 'price': str(product.price)}
    #     self.order[product_id]['quantity'] += quantity
    #     self.save_session() asli
    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.order:
            self.order[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.order[product_id]['quantity'] += quantity
        self.save_session()

    # def add(self, product, quantity):
    #     product_id = str(product.id)
    #     if product_id not in self.order:
    #         self.order[product_id] = {'quantity': 0, 'product': product}
    #     self.order[product_id]['quantity'] += quantity
    #     self.save_session()

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
