from django.core.exceptions import ValidationError
from django.db import models

from manager.models import Country, Team, Driver


class Racetrack(models.Model):
    name = models.CharField(max_length=30)
    location = models.ForeignKey(Country, on_delete=models.CASCADE)
    lap_length_km = models.FloatField()
    total_laps = models.PositiveIntegerField()
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

class Championship(models.Model):
    name = models.CharField(max_length=30)
    teams = models.ManyToManyField(Team, blank=True, related_name="league_teams")
    races = models.ManyToManyField('Race', blank=True, related_name="league_races")

    def __str__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateTimeField()
    location = models.ForeignKey(Racetrack, on_delete=models.CASCADE)
    laps = models.PositiveIntegerField()
    teams = models.ManyToManyField(Team, related_name="races")

    def __str__(self):
        return self.name
    

class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='results')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()
    best_lap = models.TimeField()

    def __str__(self):
        return f"{self.race.name} - {self.driver.name} - {self.position}"    
