from django.urls import path
from .views import SignupView,verify_email

urlpatterns = [
    path('register/',SignupView.as_view(),name='register'),
    path('verify_email/<str:email>/', verify_email, name='verify_email'),

]