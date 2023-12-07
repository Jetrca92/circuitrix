from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from races.managers import UpcomingRacesManager


# One year equals to 84 days (12 weeks) - season lasts 12 weeks, 10 weeks for races and 2 weeks for season break
DAYS_IN_A_SEASON = 84


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Staff(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField()

    class Meta:
        abstract = True

    
    def age(self):
        now = timezone.now()
        birth_date = self.date_of_birth
        age_days = (now - birth_date).days
        age_years = int (age_days / DAYS_IN_A_SEASON)
        age_days = age_days % DAYS_IN_A_SEASON
        return f"{age_years} years, {age_days} days"

    def __str__(self):
        return self.name


class Manager(models.Model):
    name = models.CharField(null=True, max_length=20, default=None, unique=True)
    avatar = models.CharField(default="manager/avatar.png", max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.OneToOneField('Team', on_delete=models.CASCADE, blank=True, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}"
    

class Team(models.Model):
    owner = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name="team_owner")
    name = models.CharField(max_length=30, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey('Country', on_delete=models.CASCADE, null=True, blank=True)
    drivers = models.ManyToManyField('Driver', blank=True, related_name="team_drivers")
    championship = models.ForeignKey('Championship', blank=True, null=True, on_delete=models.CASCADE, related_name="team_championship")
    lead_designer = models.ForeignKey('LeadDesigner', blank=True, null=True, on_delete=models.CASCADE, related_name="team_designer")
    race_mechanics = models.ManyToManyField('RaceMechanic', blank=True, related_name="team_race_mechanics")
    car = models.ForeignKey('Car', on_delete=models.CASCADE, blank=True, null=True, related_name="team_car")
    total_fans = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    

class Country(models.Model):
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=3, null=True)
    logo_location = models.CharField(max_length=50, default="manager/flags/blank.png")
    def __str__(self):
        return self.name  
    

class Driver(Staff):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="driver_team")
    experience = models.PositiveIntegerField(default=0)
    skill_overall = models.PositiveIntegerField()
    skill_racecraft = models.PositiveIntegerField()
    skill_pace = models.PositiveIntegerField()
    skill_focus = models.PositiveIntegerField()
    skill_car_management = models.PositiveIntegerField()
    skill_feedback = models.PositiveIntegerField()
    

class LeadDesigner(Staff):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="lead_designer_team")
    skill = models.PositiveIntegerField(default=5)


class RaceMechanic(Staff):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name="race_mechanic_team")
    skill = models.PositiveIntegerField(default=5)


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
    
    def update_name(self, new_name):
        self.name = new_name
        self.save()
    

class Racetrack(models.Model):
    name = models.CharField(max_length=30)
    location = models.ForeignKey(Country, on_delete=models.CASCADE)
    image_location = models.CharField(max_length=50, default="manager/circuits/blank.png")
    description = models.TextField()
    lap_length_km = models.FloatField()
    total_laps = models.PositiveIntegerField()
    lap_record = models.ForeignKey('LapRecord', on_delete=models.CASCADE, blank=True, null=True, related_name="racetrack_laprecord")
    # Percentages of different parts of track, total 100%
    straights = models.FloatField()
    slow_corners = models.FloatField()
    fast_corners = models.FloatField()

    def __str__(self):
        return self.name
    
    def clean(self):
        # Check if the sum of straights, slow_corners, and fast_corners is equal to 100
        total_percentage = self.straights + self.slow_corners + self.fast_corners
        if total_percentage != 100:
            raise ValidationError("The sum of straights, slow corners, and fast corners must be equal to 100.")

    def save(self, *args, **kwargs):
        self.clean()
        super(Racetrack, self).save(*args, **kwargs)


class LapRecord(models.Model):
    holder = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="laprecord_holder")
    racetrack = models.ForeignKey(Racetrack, on_delete=models.CASCADE, related_name="laprecord_racetrack")
    time = models.DurationField(blank=True, null=True)
    date_set = models.DateTimeField(auto_now_add=True)


class Championship(models.Model):
    name = models.CharField(max_length=30)
    division = models.PositiveIntegerField(default=1)
    teams = models.ManyToManyField(Team, blank=True, related_name="league_teams")
    races = models.ManyToManyField('Race', blank=True, related_name="league_races")
    racetracks = models.ManyToManyField(Racetrack, blank=True, related_name="league_racetracks")

    def __str__(self):
        return self.name
    
    def add_racetracks(self):
        racetracks = Racetrack.objects.all()
        self.racetracks.set(racetracks)
        

class Race(models.Model):
    name = models.CharField(max_length=60)
    date = models.DateTimeField()
    location = models.ForeignKey(Racetrack, on_delete=models.CASCADE)
    laps = models.PositiveIntegerField()
    teams = models.ManyToManyField(Team, related_name="races")

    objects = models.Manager()
    upcoming_objects = UpcomingRacesManager()

    def get_upcoming_races(self):
        return self.upcoming_objects.all()

    def __str__(self):
        return f"{self.name} ({self.date})"
    

class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='results')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(blank=True, null=True)
    best_lap = models.DurationField(blank=True, null=True)
    laps = models.ManyToManyField('Lap', blank=True, related_name="lap_race")

    def __str__(self):
        return f"{self.race.name} - {self.driver.name} - {self.position}"  


class Lap(models.Model):
    time = models.PositiveIntegerField()
    lap_number = models.PositiveIntegerField()
    race_result = models.ForeignKey(RaceResult, blank=True, null=True, on_delete=models.CASCADE, related_name="results_laps")
    position = models.PositiveIntegerField(blank=True, null=True)  
