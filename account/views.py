# from random import randint
#
# from django.http import HttpResponse
# from django.shortcuts import render
# from django.urls import reverse_lazy
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.views.generic import CreateView
from random import randint
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy, reverse
from redis import Redis
from django.views.generic import CreateView, ListView, View, DetailView, UpdateView
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from sqlite3 import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from account.models import User, Address

r = Redis(host='localhost', port=6379, decode_responses=True)
from config import settings
from .models import User


#
# class SignupView(CreateView):
#     model = User
#     template_name = 'signup.html'
#     fields = ['username', 'password', 'email']
#
#     def form_valid(self, form):
#         print('njnvknjknjkjnkjnjvrntinjvrtnjrijnbirjntbirubnir')
#         print(self.request.POST)
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         email = form.cleaned_data['email']
#
#         if User.objects.filter(email=email).exists():
#             return self.form_invalid(form)
#
#         try:
#             r.set(name=username, value=password)
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()
#
#             otp_code = ''.join([str(randint(0, 9)) for _ in range(6)])
#             r.set(name=f"{user.id}", value=f"{otp_code}")
#             print(otp_code)
#
#             subject = 'Verification code'
#             message = f'Your verification code is: {otp_code}'
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [user.email, ]
#             send_mail(subject, message, email_from, recipient_list)
#             return super().form_valid(form)
#         except IntegrityError:
#             return self.form_invalid(form)
#
#     @property
#     def success_url(self):
#         return reverse_lazy('verify_email', kwargs={'email': self.object.email})


class SignupView(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not all([username, password, email]):
            return messages.error(request, "please fill al blanks")

        if User.objects.filter(email=email).exists():
            return messages.error(request, 'this email already exist')

        if User.objects.filter(username=username).exists():
            return messages.error(request, 'this username already exist')

        try:
            r.set(name=username, value=password)
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()

            otp_code = ''.join([str(randint(0, 9)) for _ in range(6)])
            r.set(name=str(user.id), value=otp_code)
            print(otp_code)

            subject = 'Verification code'
            message = f'Your verification code is: {otp_code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect(reverse('verify_email', kwargs={'email': email}))
        except IntegrityError:
            messages.error(request, 'An error occurred')

class ChangePassword(UpdateView):
    model = User
    fields = ['password']
    success_url = reverse_lazy('products')


class VerifyEmailForChangePassword(View):
    def get(self, request):
        return render(request, 'login_with_email.html')

    def post(self, request):
        email = request.POST.get('email', False)

        try:
            print('nenvekjrnfilwjkervnekjrnfveikjrnvekjdrnfd ')
            user = User.objects.get(email=email)
            otp_code = ''.join([str(randint(0, 9)) for _ in range(6)])
            print(otp_code)
            r.set(name=f"{user.id}", value=f"{otp_code}")
            subject = 'Verification code'
            message = f'Your verification code is: {otp_code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            return redirect(reverse('verify_email', kwargs={'email': email}))
        except ObjectDoesNotExist:
            messages.error(request, "This email does not exist. You need to create an account first!")
            return render(request, 'login_with_email.html')
class SignInWithEmail(View):
    def get(self, request):
        return render(request, 'login_with_email.html')

    def post(self, request):
        email = request.POST.get('email', False)

        try:
            print('nenvekjrnfilwjkervnekjrnfveikjrnvekjdrnfd ')
            user = User.objects.get(email=email)
            otp_code = ''.join([str(randint(0, 9)) for _ in range(6)])
            print(otp_code)
            r.set(name=f"{user.id}", value=f"{otp_code}")
            subject = 'Verification code'
            message = f'Your verification code is: {otp_code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            return redirect(reverse('verify_email', kwargs={'email': email}))
        except ObjectDoesNotExist:
            messages.error(request, "This email does not exist. You need to create an account first!")
            return render(request, 'login_with_email.html')


class SignInWithEmail(View):
    def get(self, request):
        return render(request, 'login_with_email.html')

    def post(self, request):
        email = request.POST.get('email', False)

        try:
            print('nenvekjrnfilwjkervnekjrnfveikjrnvekjdrnfd ')
            user = User.objects.get(email=email)
            otp_code = ''.join([str(randint(0, 9)) for _ in range(6)])
            print(otp_code)
            r.set(name=f"{user.id}", value=f"{otp_code}")
            subject = 'Verification code'
            message = f'Your verification code is: {otp_code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            return redirect(reverse('verify_email', kwargs={'email': email}))
        except ObjectDoesNotExist:
            messages.error(request, "This email does not exist. You need to create an account first!")
            return render(request, 'login_with_email.html')


class SignInWithUsernameAndPassword(View):
    def get(self, request):
        return render(request, 'login_with_username_and_password.html')

    def post(self, request):
        try:
            username = request.POST['username']
            user = User.objects.get(username=username)
            print(request)
            login(request, user)
            user.is_verified = True
            messages.success(request, 'logged in successfully', 'success')
            return redirect('products')
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password. Please try again.")
            return render(request, 'login_with_username_and_password.html')


def verify_email(request, email):
    if request.method == 'POST':
        user_otp = request.POST.get('otp_code')
        user = User.objects.get(email=email)
        otp = r.get(f'{user.id}')
        if otp == user_otp:
            user.is_active = True
            user.save()
            password = r.get(user.username)
            print(user.username, password)
            login(request, user)
            return redirect('register')
        else:
            return render(request, 'verify_email.html', {'error_message': 'invalid otp code.'})
    else:
        return render(request, 'verify_email.html')


class LogoutUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, "You have been logged out successfully.")
        return redirect('products')

class UserProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        address = Address.objects.filter(costumer=user)
        context['addresses'] = address
        return context





class ChaneProfileView(UpdateView):
        model = User
        fields = ['username','first_name','last_name']
        template_name = 'change_profile.html'

        def get_success_url(self):
            return reverse_lazy('profile', kwargs={'pk': self.object.pk})



