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


class CategoryTestCase(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(name='Electronics')

        self.child_category = Category.objects.create(name='Laptops', sub_category=self.parent_category)

    def test_category_str_method(self):

        expected_parent_str = self.parent_category.name
        self.assertEqual(str(self.parent_category), expected_parent_str)

        expected_child_str = f"{self.child_category.sub_category}----{self.child_category.name}"
        self.assertEqual(str(self.child_category), expected_child_str)

