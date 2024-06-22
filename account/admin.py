from django.contrib import admin

from order.models import Order, OrderItem
from product.models import Category, Discount, DiscountCode, Image, Product

from .models import Address, User, UserProfile

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


class CustomUserAdmin(admin.ModelAdmin):
    model = User

    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, CustomUserAdmin)
