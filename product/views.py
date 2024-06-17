from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from order.forms import CartItemQuantityForm
from .models import Product, Image, Category


# product list view for displaying products
class ProductsListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        product_images = {}
        for product in products:
            product_images[product] = Image.objects.filter(product=product)
        context['product_images'] = product_images
        return context


# for displaying product's detail
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'
    lookup_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CartItemQuantityForm()
        context['form'] = form
        return context


# for display category tree
class CategoryTreeView(ListView):
    model = Category
    template_name = 'category_tree.html'
    context_object_name = "category"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        top_categories = Category.objects.filter(parent__isnull=True)

        categories_with_subcategories = []
        for category in top_categories:
            category_data = {
                'category': category,
                'subcategories': category.child.all()
            }
            categories_with_subcategories.append(category_data)

        context['categories_data'] = categories_with_subcategories
        return context


# for displaying each category products
class SubcategoryAndProducts(View):
    def get(self, request, id):
        category = Category.objects.get(id=id)
        products = Product.objects.filter(category=category)
        product_data = []
        for product in products:
            images = Image.objects.filter(product=product)
            product_data.append((product, images))
        return render(request, 'category_products.html', {'category': category, 'product_data': product_data})
