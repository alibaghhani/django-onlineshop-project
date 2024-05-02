from random import randint
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from random import randint
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy, reverse
from redis import Redis
from django.views.generic import CreateView, ListView, View
from django.contrib.auth import login, logout, authenticate
from django.conf import settings
from sqlite3 import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from account.models import User
r = Redis(host='localhost', port=6379, decode_responses=True)
from config import settings
from .models import User


class SignupView(CreateView):
    model = User
    template_name = 'signup.html'
    fields = ['username', 'password', 'email']

    def form_valid(self, form):
        print('njnvknjknjkjnkjnjvrntinjvrtnjrijnbirjntbirubnir')
        print(self.request.POST)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            return self.form_invalid(form)

        try:
            r.set(name=username, value=password)
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            otp_code = ''.join([str(randint(0, 9)) for _ in range(6)])
            r.set(name=f"{user.id}", value=f"{otp_code}")
            print(otp_code)

            subject = 'Verification code'
            message = f'Your verification code is: {otp_code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return super().form_valid(form)
        except IntegrityError:
            return self.form_invalid(form)

    @property
    def success_url(self):
        return reverse_lazy('verify_email', kwargs={'email': self.object.email})


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
            return redirect('signup')
        else:
            return render(request, 'verify_email.html', {'error_message': 'invalid otp code.'})
    else:
        return render(request, 'verify_email.html')