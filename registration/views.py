from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.dispatch import receiver
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from allauth.account.signals import user_signed_up
from manager.models import User
from registration.forms import RegistrationForm, LoginForm, CustomPasswordResetForm, CustomSetPasswordForm


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
                    self.send_welcome_email(email)
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

    def send_welcome_email(self, email):
        subject = 'Welcome to Circuitrix!'
        message = 'Greetings! You have successfully registered on our portal. Good luck!'
        from_email = 'settings.EMAIL_HOST_USER'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)


@transaction.atomic
def register(request):
    if request.method != "POST":
        return render(request, "registration/register.html")

    username = request.POST["username"]  
    email = request.POST["email"]

    # Ensure password matches confirmation
    password = request.POST["password1"]
    confirmation = request.POST["password2"]
    if password != confirmation:
        return render(request, "registration/register.html", {
            "message": "Passwords must match."
        })

    # Attempt to create new user
    try:
        user = User.objects.create_user(username, email, password)
        user.save()
    except IntegrityError:
        return render(request, "registration/register.html", {
            "message": "Username already taken."
        })
        
    # Create users manager model ...
    #TO DO

    # Logs the user in and sends welcome email
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    send_mail(
        'Welcome to Circuitrix!',
        'Greetings! You have successfully registered on our portal. Good luck!',
        'settings.EMAIL_HOST_USER',
        [f"{email}"],
        fail_silently=True
    )
    return HttpResponseRedirect(reverse("manager:index"))

    
# Sends welcome email if user signs up with google acc    
@receiver(user_signed_up)
def send_google_registration_email(request, user, **kwargs):
    if user.socialaccount_set.filter(provider='google').exists():

        email = user.email
        send_mail(
            'Welcome to Circuitrix!',
            'Greetings! You have successfully registered on our portal. Good luck!',
            'settings.EMAIL_HOST_USER',
            [f"{email}"],
            fail_silently=True
        )
    return HttpResponseRedirect(reverse("manager:index"))


class CustomLoginView(LoginView):
    form_class = LoginForm


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm