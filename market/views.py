from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from manager.models import Driver
from market.forms import ListDriverForm, FireDriverForm
from market.helpers import list_driver
from market.models import DriverListing
from races.views import ManagerContextMixin


class DriverMarketView(LoginRequiredMixin, ManagerContextMixin, View):
    template_name = "market/market.html"

    def get(self, request):
        listed_drivers = DriverListing.objects.all()
        context = super().get_context_data()
        context["listed_drivers"] = listed_drivers
        return render(request, self.template_name, context)
    

class ListDriverView(LoginRequiredMixin, ManagerContextMixin, View):
    
    def post(self, request, id):
        form = ListDriverForm(request.POST)
        if form.is_valid():
            list_driver(id, form.cleaned_data["price"])
        return HttpResponseRedirect(reverse("teams:driver_page", kwargs={'id': id}))
        

class FireDriverView(LoginRequiredMixin, ManagerContextMixin, View):
    
    def post(self, request, id):
        form = FireDriverForm()
        if form.is_valid():
            driver = Driver.objects.get(id=id)
            driver.terminate_contract()
            list_driver(id, 0)
        return HttpResponseRedirect(reverse("teams:driver_page", kwargs={'id': id}))
    

