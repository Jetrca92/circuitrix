from django.db.models import Max
from django.utils import timezone

from manager.models import Driver
from manager.models import DAYS_IN_A_SEASON
from market.models import DriverListing, Bid

def list_driver(id, price):
    driver = Driver.objects.get(id=id)
    dl = DriverListing(
        driver=Driver.objects.get(id=id),
        seller=driver.team,
        price=price,
    )
    dl.save()
    driver.list()


def bid_driver(id, bidder, bid):
    dl = DriverListing.objects.get(driver=Driver.objects.get(id=id))
    bid = Bid(
        driver_listing=dl,
        bidder=bidder,
        amount=bid,
    )
    bid.save()


def sell_driver(id, driver_listing):
    highest_bid = Bid.objects.filter(driver_listing=driver_listing).order_by('-amount').first()
    driver = Driver.objects.get(id=id)
    # Change driver owner, unlist driver, deactivate driver_listing
    driver_listing.close()
    if highest_bid:
        driver.sell(highest_bid.bidder)
        return
    driver.unlist()


def get_u21_driver_listings():
    twenty_one_game_years_ago = timezone.now() - timezone.timedelta(days=21 * DAYS_IN_A_SEASON)
    return DriverListing.objects.filter(is_active=True, driver__date_of_birth__gt=twenty_one_game_years_ago)