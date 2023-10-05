from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Manager(models.Model):
    name = models.CharField(null=True, max_length=20, default=None, unique=True)
    avatar = models.CharField(default="manager/avatar.png", max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}"
    

class Team(models.Model):
    owner = models.ForeignKey(Manager, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    total_fans = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return self.name