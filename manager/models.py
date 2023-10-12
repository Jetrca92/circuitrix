from datetime import timezone

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
    location = models.ForeignKey('Country', on_delete=models.CASCADE, null=True, blank=True)
    drivers = models.ManyToManyField('Driver', blank=True, related_name="team_drivers")
    lead_designer = models.ForeignKey('LeadDesigner', blank=True, null=True, on_delete=models.CASCADE, related_name="team_designer")
    race_mechanics = models.ManyToManyField('RaceMechanic', blank=True, related_name="team_race_mechanics")
    total_fans = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    

class Country(models.Model):
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=3)
    logo_location = models.CharField(max_length=50, default="manager/united_kingdom.png")

    def __str__(self):
        return self.name  
    

class Driver(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="driver_team")
    experience = models.PositiveIntegerField(default=0)
    skill_overall = models.PositiveIntegerField()
    skill_racecraft = models.PositiveIntegerField()
    skill_pace = models.PositiveIntegerField()
    skill_focus = models.PositiveIntegerField()
    skill_car_management = models.PositiveIntegerField()
    skill_feedback = models.PositiveIntegerField()

    def age(self):
        now = timezone.now()
        birth_date = self.date_of_birth
        age_days = (now - birth_date).days
        age_years = int (age_days / 84)
        age_days = age_days % 84
        return f"{age_years} years, {age_days} days"

    def __str__(self):
        return self.name
    

class LeadDesigner(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="lead_designer_team")
    skill = models.PositiveIntegerField(default=5)

    def age(self):
        now = timezone.now()
        birth_date = self.date_of_birth
        age_days = (now - birth_date).days
        age_years = int (age_days / 84)
        age_days = age_days % 84
        return f"{age_years} years, {age_days} days"

    def __str__(self):
        return self.name


class RaceMechanic(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="race_mechanic")
    skill = models.PositiveIntegerField(default=5)

    def age(self):
        now = timezone.now()
        birth_date = self.date_of_birth
        age_days = (now - birth_date).days
        age_years = int (age_days / 84)
        age_days = age_days % 84
        return f"{age_years} years, {age_days} days"

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=30, default="Car")
    owner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="car_owner")
    engine = models.PositiveIntegerField(default=5)
    gearbox = models.PositiveIntegerField(default=5)
    brakes = models.PositiveIntegerField(default=5)
    front_wing = models.PositiveIntegerField(default=5)
    suspension = models.PositiveIntegerField(default=5)
    rear_wing = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name