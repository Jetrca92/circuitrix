from django.urls import path

from market.views import DriverMarketView, SellDriverView

app_name = "market"

urlpatterns = [
    path("drivers-market", DriverMarketView.as_view(), name="driver_market"),
    path("sell-driver/<int:id>", SellDriverView.as_view(), name="sell_driver"),
]
