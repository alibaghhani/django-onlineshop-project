from django.contrib import admin
from .models import User,Address
from product.models import Image,Category,Product
from order.models import OrderItem,Order
# Register your models here.
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)