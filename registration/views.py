from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.db import IntegrityError, transaction
from django.dispatch import receiver
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from allauth.account.signals import user_signed_up
from manager.models import User
from registration.forms import RegistrationForm, LoginForm, CustomPasswordResetForm, CustomSetPasswordForm
from registration.helpers import send_welcome_email


class RegisterView(View):
    template_name = "registration/register.html"

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {"form": form})

    @transaction.atomic
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password1"]
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    
                    # Create users manager model ...
                    # TO DO
                    
                    # Log user in and Send welcome email
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    send_welcome_email(email)
                return HttpResponseRedirect(reverse("manager:index"))
            except IntegrityError:
                return render(request, self.template_name, {
                    "message": "Integrity Error!"
                })
        else:
            # Handle the case when the form is not valid
            return render(request, self.template_name, {
                "form": form,
            })
    

# Sends welcome email if user signs up with google acc    
@receiver(user_signed_up)
def send_google_registration_email(request, user, **kwargs):
    if user.socialaccount_set.filter(provider='google').exists():
        email = user.email
        send_welcome_email(email)
        # Create users manager model ...
        # TO DO
    return HttpResponseRedirect(reverse("manager:index"))


class CustomLoginView(LoginView):
    form_class = LoginForm


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm