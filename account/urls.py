from django.urls import path

from .views import (AddAddressView, AdminPannel, AllUsersAddresses,
                    ChaneProfileView, DeleteAddressView, DeleteUserOrder,
                    LoginChoice, LogoutUser, ResetPasswordDoneView,
                    ResetPasswordView, SignInWithEmail,
                    SignInWithUsernameAndPassword, SignupView,
                    UserOrderDetailView, UserOrdersView,
                    UserPasswordResetCompleteView,
                    UserPasswordResetConfirmView, UserProfileView,
                    verify_email)

urlpatterns = [
    # routes related to user authentication---------

    path('register/', SignupView.as_view(), name='register'),
    path('verify_email/<str:email>/', verify_email, name='verify_email'),
    path('loginwithemail/', SignInWithEmail.as_view(), name='email_login'),
    path('loginwitthusername/', SignInWithUsernameAndPassword.as_view(), name='username_login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('choice_login_way/', LoginChoice.as_view(), name="login_choice"),

    # routes related to change password-----------

    path('reset_pass/', ResetPasswordView.as_view(), name="reset_password"),
    path('reset/done/', ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('confirm/complete', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # routes related to user profile-------------

    path('profile/<int:pk>/', UserProfileView.as_view(), name='profile'),
    path('change_personal_information/<int:pk>/', ChaneProfileView.as_view(), name="change_profile"),
    path('userorder/', UserOrdersView.as_view(), name='user-orders'),
    path('userorderdetail/<int:pk>/', UserOrderDetailView.as_view(), name='user-order-detail'),
    path('deleteorder/<int:pk>/', DeleteUserOrder.as_view(), name='delete-user-order'),

    # routes related to user's address-------------

    path('user_address/', AllUsersAddresses.as_view(), name='all_addresses'),
    path('add_new_address/', AddAddressView.as_view(), name="add_address"),
    path('delete-address/<int:pk>/', DeleteAddressView.as_view(), name='delete_address'),

    path('AdminPannel/', AdminPannel.as_view(), name='Admin')

]
