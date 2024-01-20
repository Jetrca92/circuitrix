from django.db import models

from manager.models import Driver, Team


class DriverListing(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name="driver_listing")
    seller = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    price = models.IntegerField()
    date_listed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver.surname}"


class Bid(models.Model):
    driver_listing = models.ForeignKey(DriverListing, on_delete=models.CASCADE, related_name="bid")
    bidder = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="bidder")
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.bidder.name} on {self.driver_listing.driver.surname} for ${self.amount}"