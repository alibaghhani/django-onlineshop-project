from django.contrib import admin
from .models import User,Address
from product.models import Image,Category,Product
# Register your models here.
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Product)