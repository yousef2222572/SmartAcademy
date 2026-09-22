from django.contrib.auth.views import LoginView
from django.urls import path,include
from .views import EditProfile, ForgotPasswordView, register_view,UserLoginView,otpcodeView,ChangePasswordView,OtpcodeViewForgotPassword
from .forms import UserLoginForm
from django.contrib.auth.views import LogoutView

urlpatterns=[
    path('profile/',EditProfile, name='profile'),    
    path('otpcode/', otpcodeView, name='otpcode'),
    path('otpcodeforgotpassword/', OtpcodeViewForgotPassword, name='otpcode.forgotpassword'),
    path('forgotpassword/',ForgotPasswordView.as_view(), name='forgot_password'),
    path('logup/',register_view.as_view(), name='Register'),
    path('login/',UserLoginView.as_view(), name='login_form'),
    path('change_password/',ChangePasswordView.as_view(), name='change_password'),
    # path('forgot_password/',forgot_passwordView.as_view(), name='forgot_password'),
    path('accounts',include('django.contrib.auth.urls'))
]