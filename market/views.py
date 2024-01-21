from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from manager.models import Driver, Team
from market.forms import ListDriverForm, FireDriverForm, DriverBidForm
from market.helpers import list_driver, bid_driver
from market.models import DriverListing
from races.views import ManagerContextMixin
from teams.views import DriverPageView


class FormHandlingMixin:
    #TO DO
    pass
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
        form = FireDriverForm(request.POST)
        if form.is_valid():
            driver = Driver.objects.get(id=id)
            driver.terminate_contract()
            list_driver(id, 0)
            return HttpResponseRedirect(reverse("teams:driver_page", kwargs={'id': id}))
        return HttpResponseRedirect(reverse("manager:index"))
    

class BidDriverView(LoginRequiredMixin, ManagerContextMixin, View):

    def post(self, request, id):
        form = DriverBidForm(request.POST)
        if form.is_valid():
            context = super().get_context_data()
            bidder = Team.objects.get(manager=context["current_user_manager"])
            bid_driver(id, bidder, form.cleaned_data["amount"])
            return HttpResponseRedirect(reverse("teams:driver_page", kwargs={'id': id}))
        
        # Form is not valid, render DriverPageView with the error form
        # This seems like a lot of work to have BidDriverView seperate from DriverPageView ? it works tho -.-
        driver_page_view = DriverPageView()
        driver_page_view.request = HttpRequest()
        driver_page_view.request.method = "GET"
        driver_page_view.request.user = request.user
        driver_page_view.kwargs = {'id': id}
        driver = driver_page_view.get_object()
        form_fire = FireDriverForm()
        form_sell = ListDriverForm()
        form_bid = DriverBidForm(request.POST, initial={"driver_listing": DriverListing.objects.get(driver=driver)})
        context = driver_page_view.get_context_data()
        context.update({"driver": driver, "form_fire": form_fire, "form_sell": form_sell, "form_bid": form_bid})
        return render(request, driver_page_view.template_name, context)
    

