from django.urls import path

from market.views import DriverMarketView, SellDriverView, FireDriverView

app_name = "market"

urlpatterns = [
    path("drivers-market", DriverMarketView.as_view(), name="driver_market"),
    path("sell-driver/<int:id>", SellDriverView.as_view(), name="sell_driver"),
    path("fire-driver/<int:id>", FireDriverView.as_view(), name="fire_driver"),
]
