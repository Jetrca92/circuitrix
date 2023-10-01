from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from allauth.account.signals import user_signed_up
from manager.helpers import random_password
from manager.models import User, Manager


@transaction.atomic
def login_view(request):
    if request.method != "POST":
        return render(request, "registration/login.html")

    # Attempt to sign user in
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
        login(request, user)
        # Check for first login
        manager, created = Manager.objects.get_or_create(
            name=user.username,
            user=user,
        )
        if created:
            # redirect to choose team, name etc
            pass
        manager.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request, "registration/login.html", {
        "message": "Invalid username and/or password."
    }) 


@transaction.atomic
def forgot_password(request):
    if request.method != "POST":
        return render(request, "registration/forgot_password.html")
    
    email = request.POST["email"]
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return render(request, "registration/forgot_password.html", {
            "message": "Email not valid!"
        })
    new_password = random_password()
    user.set_password(new_password)
    user.save()
    send_mail(
        'Forgotten password',
        f'Greetings! Your new password: {new_password}',
        'settings.EMAIL_HOST_USER',
        [f"{email}"],
        fail_silently=True
    )
    return render(request, "registration/forgot_password.html", {
        "message": "An email with instructions on how to reset your password has been sent."
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@transaction.atomic
def register(request):
    if request.method != "POST":
        return render(request, "registration/register.html")

    username = request.POST["username"]  
    email = request.POST["email"]

    # Ensure password matches confirmation
    password = request.POST["password"]
    confirmation = request.POST["confirmation"]
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
    #create_resident_and_warehouse(user)

    # Logs the user in and sends welcome email
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    send_mail(
        'Welcome to Circuitrix!',
        'Greetings! You have successfully registered on our portal. Good luck!',
        'settings.EMAIL_HOST_USER',
        [f"{email}"],
        fail_silently=True
    )
    return HttpResponseRedirect(reverse("index"))

    
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
    return HttpResponseRedirect(reverse("index"))