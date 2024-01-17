from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from manager.models import Driver
from market.forms import SellDriverForm
from market.helpers import list_driver
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
    

class SellDriverView(LoginRequiredMixin, ManagerContextMixin, View):
    
    def post(self, request, id):
        form = SellDriverForm(request.POST)
        if form.is_valid():
            list_driver(id, form.cleaned_data["price"])
        return HttpResponseRedirect(reverse("teams:driver_page", kwargs={'id': id}))
        


class FireDriverView(LoginRequiredMixin, ManagerContextMixin, View):
    form = SellDriverForm()

    def post(self, request, id):
        pass
    

