"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.context_processors import static
from django.urls import path,include

from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/',include('account.urls')),
    path('',include('product.urls')),
    path('order/',include('order.urls')),
    path('apiorder/',include('order.api_urls')),
    path('api_authentication/',include('account.api_urls'))
]
 # "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNjQ2NjM3NCwiaWF0IjoxNzE2Mzc5OTc0LCJqdGkiOiIyMWIxNjI4YTVlMGQ0MmQzYjE0MTQyNDYzYWRjOTc5NSIsInVzZXJfaWQiOjF9.-Le1hKKa5o-iBwbwkmAydwyubYmGAARlCoeS_hVRMIM",
 #    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2MzgwMjc0LCJpYXQiOjE3MTYzNzk5NzQsImp0aSI6IjYyY2E0N2E4NjQwMzQzYWZiMzUwYTA1OTczMmViNWU1IiwidXNlcl9pZCI6MX0.UfybUnEIfeGltIkdHdKnI2hvTl_sJPSJDkmBMIiFpyw"
