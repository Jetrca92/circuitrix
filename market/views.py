from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render

from manager.models import Driver
from market.models import DriverListing
from races.views import ManagerContextMixin

class DriverMarketView(LoginRequiredMixin, ManagerContextMixin, View):
    template_name = "market/market.html"

    def get(self, request):
        driver = Driver.objects.all().first()
        dl = DriverListing(
            driver=driver,
            seller=driver.team,
            price=100,
        )
        dl.save()
        listed_drivers = DriverListing.objects.all()
        context = {"listed_drivers": listed_drivers}
        return render(request, self.template_name, context)
    

