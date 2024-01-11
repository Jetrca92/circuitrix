from django.urls import path

from market.views import DriverMarketView

app_name = "market"

urlpatterns = [
    path("drivers-market", DriverMarketView.as_view(), name="driver_market"),
]
