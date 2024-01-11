from django.db import models

from manager.models import Driver, Team

class DriverListing(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    seller = models.ForeignKey(Team, on_delete=models.CASCADE)
    price = models.IntegerField()
    date_listed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver.surname} ({self.seller.name})"