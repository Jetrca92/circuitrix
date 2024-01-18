from manager.models import Driver
from market.models import DriverListing

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