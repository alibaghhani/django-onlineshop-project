from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Product, Image, Category


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


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'



class CategoryTreeView(View):
    def get(self, request):
        categories = Category.objects.filter(sub_category__isnull=True)

        category_and_subcategory = {}
        for category in categories:
            if category.sub_category:
                subcategories = category.sub_category.all()
            else:
                subcategories = None
            category_and_subcategory[category] = subcategories

        return render(request, 'category_tree.html', {'category_dict': category_and_subcategory})
