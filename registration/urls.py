from django.urls import path
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from .views import RegistrationView

app_name = 'registration'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('logout/', LogoutView.as_view(), name="logout"),
]