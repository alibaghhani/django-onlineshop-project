from django.contrib import admin
from .models import User, Address, UserProfile
from product.models import Image,Category,Product,Discount,DiscountCode
from order.models import OrderItem,Order
# Register your models here.
admin.site.register(Address)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Discount)
admin.site.register(DiscountCode)
admin.site.register(UserProfile)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User

admin.site.register(User, CustomUserAdmin)
