from random import randint
from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from redis import Redis
from django.views.generic import View, DetailView, UpdateView, ListView, CreateView, TemplateView, DeleteView
from django.contrib.auth import login, logout
from django.conf import settings
from sqlite3 import IntegrityError
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from account.models import User, Address, UserProfile
from config import settings

'---- redis setup ----'
r = Redis(host='redis', port=6379, decode_responses=True)
'---------------------'

"""---- signup view ----"""


class SignupView(View):
    """
    In the get method,
    we render the page for the user,
    and then in the post method,
    we get the user's information,
    and then check whether the information already exists,
    and then in Redis, we store the user's name and lastname in Redis,
    and then enter the user record in the database.
    We generate the code, email it and save it in Redis.
    """

    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not all([username, password, email]):
            messages.error(request, "please fill al blanks")
            return render(request, self.template_name)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'this email already exist')
            return render(request, self.template_name)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'this username already exist')
            return render(request, self.template_name)

        try:
            r.set(name=username, value=password)
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(first_name=None, last_name=None, gender=None, user=user)
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
            self.request.session['user_information'] = {
                "username": user.username,
                "email": user.email
            }
            self.request.session.modified = True
            return redirect(reverse('verify_email', kwargs={'email': email}))
        except IntegrityError:
            messages.error(request, 'An error occurred')


"""--------------------------------------------------------------------------------------------"""

"""---- sign in with email view ---------------------------------------------------------------"""


class SignInWithEmail(View):

    def get(self, request):
        return render(request, 'login_with_email.html')

    def post(self, request):
        email = request.POST.get('email')

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
        except User.MultipleObjectsReturned:
            messages.error(request, "Multiple users found with the same email. Please contact support.")
            return render(request, 'login_with_email.html')
        except ObjectDoesNotExist:
            messages.error(request, "This email does not exist. You need to create an account first!")
            return render(request, 'login_with_email.html')


"""-----------------------------------------------------------------------------------------------"""

"""---- signin with username and password---------------------------------------------------------"""


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


"""--------------------------------------------------------------------------------------------------"""

"""---- verify email and otp to authenticate --------------------------------------------------------"""


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
            return redirect('products')
        else:
            return render(request, 'verify_email.html', {'error_message': 'invalid otp code.'})
    else:
        return render(request, 'verify_email.html')


"""------------------------------------------------------------------------------------------------"""

"""---- logout user view --------------------------------------------------------------------------"""


class LogoutUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, "You have been logged out successfully.")
        return redirect('products')


"""-----------------------------------------------------------------------------------------------"""

"""---- user profile view for displaying user's information and addresses  ----------------------"""


class UserProfileView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        address = Address.objects.filter(costumer=user).last()
        user_information = UserProfile.objects.filter(user_id=user.id).first()
        context['addresses'] = address
        context['user_information'] = user_information
        return context


"""----------------------------------------------------------------------------------------------"""

"""displaying all user's addresses in address page ----------------------------------------------"""


class AllUsersAddresses(ListView):
    model = Address
    template_name = 'users_addresses.html'
    context_object_name = 'addresses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.id
        addresses = Address.objects.filter(costumer=user)
        context['addresss'] = addresses
        return context


"""---------------------------------------------------------------------------------------------"""

"""---- login choice (login with email or login with username) ---------------------------------"""


class LoginChoice(TemplateView):
    template_name = 'login_choice.html'


"""---------------------------------------------------------------------------------------------"""

"""---- address view for displaying all user's addresses ---------------------------------------"""


class AddAddressView(CreateView):
    model = Address
    template_name = 'add_address.html'
    fields = ['province', 'city', 'street', 'alley', 'house_number', "full_address"]
    success_url = reverse_lazy('products')

    def form_valid(self, form):
        form.instance.costumer = self.request.user
        return super().form_valid(form)


"""-------------------------------------------------------------------------------------------"""

"""---- delete address view ------------------------------------------------------------------"""


class DeleteAddressView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('delete_addresses_success')
    login_url = reverse_lazy('login_choice')

    def get_queryset(self):
        return self.request.user.costumer_address.all()


"""------------------------------------------------------------------------------------------"""

"""---- change profile view -----------------------------------------------------------------"""


class ChaneProfileView(UpdateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'gender']
    template_name = 'change_profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(UserProfile, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.user.pk})


"""-----------------------------------------------------------------------------------------"""

"""views related to reset password ---------------------------------------------------------"""


class ResetPasswordView(views.PasswordResetView):
    template_name = 'reset_password/reset_password.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'reset_password/password_reset_email.html'


class ResetPasswordDoneView(views.PasswordResetDoneView):
    template_name = "reset_password/password_reset_done.html"


class UserPasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'reset_password/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class UserPasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'reset_password/password_reset_complete.html'


"""-----------------------------------------------------------------------------------------"""


class AdminPannel(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser == False:
            return HttpResponse('nigga fuck that child')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        return HttpResponse('my admin nigga')
