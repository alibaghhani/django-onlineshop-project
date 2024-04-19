from django.test import TestCase
from .models import Product, Category


class ProductTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')

        self.product = Product.objects.create(
            name='Laptop',
            price=1000,
            title='High-Performance Laptop',
            category=self.category
        )

    def test_product_str_method(self):
        expected_str = f"{self.product.category}----{self.product.name}"
        self.assertEqual(str(self.product), expected_str)


