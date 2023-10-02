from django.contrib.auth import login
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from allauth.account.signals import user_signed_up
from manager.models import User


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


