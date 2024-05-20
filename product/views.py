from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from order.forms import CartItemQuantityForm
from order.models import Order, OrderItem
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CartItemQuantityForm()
        context['form'] = form
        return context



#
#
# class CategoryTreeView(View):
#     def get(self, request):
#         categories = Category.objects.filter(sub_category__isnull=True)
#
#         category_and_subcategory = {}
#         for category in categories:
#             if category.sub_category:
#                 subcategories = category.sub_category.all()
#             else:
#                 subcategories = None
#             category_and_subcategory[category] = subcategories
#
#         return render(request, 'category_tree.html', {'category_dict': category_and_subcategory})
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


class SubcategoryAndProducts(View):
    def get(self,request,id):
        category = Category.objects.get(id=id)
        products = Product.objects.filter(category=category)
        return render(self.request,'category_products.html',{'category': category,'prodcut':products})






