from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, LogoutView
from . import views
from registration.views import RegisterView

app_name = 'registration'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('password_reset/', PasswordResetView.as_view(success_url=reverse_lazy('registration:password_reset_done')), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(success_url=reverse_lazy('registration:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('logout/', LogoutView.as_view(), name='logout'),
]