from django.contrib.auth import views as auth_views
from django.urls import path
from .views_front import LoginView, ProfileView, RegisterView, OTPVerifyView, PasswordResetRequestView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify_otp'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
