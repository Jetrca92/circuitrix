from django.db import models
from django.utils import timezone

class UpcomingRacesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(date__gt=timezone.now())