from django.urls import path

from market.views import DriverMarketView, ListDriverView, FireDriverView, BidDriverView

app_name = "market"

urlpatterns = [
    path("drivers-market", DriverMarketView.as_view(), name="driver_market"),
    path("sell-driver/<int:id>", ListDriverView.as_view(), name="list_driver"),
    path("fire-driver/<int:id>", FireDriverView.as_view(), name="fire_driver"),
    path("bid_driver/<int:id>", BidDriverView.as_view(), name="bid_driver"),
]
