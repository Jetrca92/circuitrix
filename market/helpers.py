from django.db.models import Max

from manager.models import Driver
from market.models import DriverListing, Bid

def list_driver(id, price):
    driver = Driver.objects.get(id=id)
    dl = DriverListing(
        driver=Driver.objects.get(id=id),
        seller=driver.team,
        price=price,
    )
    dl.save()
    driver.is_market_listed = True
    driver.save()

def bid_driver(id, bidder, bid):
    dl = DriverListing.objects.get(driver=Driver.objects.get(id=id))
    bid = Bid(
        driver_listing=dl,
        bidder=bidder,
        amount=bid,
    )
    bid.save()

def sell_driver(id, driver_listing):
    highest_bid = Bid.objects.filter(driver_listing=driver_listing).aggregate(Max('amount'))['amount__max']
    driver = Driver.objects.get(id=id)
    # Set driver_listing to inactive
    driver_listing.is_active = False
    driver_listing.save()
    driver.is_market_listed = False
    driver.save()

    # Change driver_owner
    


