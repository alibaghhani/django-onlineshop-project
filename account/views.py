from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User

# Create your views here.
class SignupView(CreateView):
    model = User
    template_name = 'signup.html'
    fields = ['username', 'password', 'email']

    def form_valid(self, form):
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

