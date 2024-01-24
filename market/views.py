from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from manager.models import Driver, Team
from market.forms import ListDriverForm, FireDriverForm, DriverBidForm
from market.helpers import list_driver, bid_driver, sell_driver
from market.models import DriverListing
from races.views import ManagerContextMixin
from teams.views import DriverPageView


class DriverMarketView(LoginRequiredMixin, ManagerContextMixin, View):
    template_name = "market/market.html"

    def get(self, request):
        listed_drivers = DriverListing.objects.all()
        context = super().get_context_data()
        context["listed_drivers"] = listed_drivers
        return render(request, self.template_name, context)
    

class FormHandlingMixin:
    # This seems like a lot of work to have BidDriverView seperate from DriverPageView ? it works tho -.-
    def handle_invalid_form(self, request, id, form_fire=None, form_sell=None, form_bid=None):
        driver_page_view = DriverPageView()
        driver_page_view.request = HttpRequest()
        driver_page_view.request.method = "GET"
        driver_page_view.request.user = request.user
        driver_page_view.kwargs = {'id': id}
        driver = driver_page_view.get_object()
        form_fire = form_fire or FireDriverForm() 
        form_sell = form_sell or ListDriverForm()
        form_bid = form_bid or DriverBidForm(initial={"driver_listing": DriverListing.objects.get(driver=driver)})
        context = driver_page_view.get_context_data()
        context.update({"driver": driver, "form_fire": form_fire, "form_sell": form_sell, "form_bid": form_bid})
        return render(request, driver_page_view.template_name, context)
    

class ListDriverView(LoginRequiredMixin, ManagerContextMixin, FormHandlingMixin, View):
    
    def post(self, request, id):
        form = ListDriverForm(request.POST)
        if form.is_valid():
            list_driver(id, form.cleaned_data["price"])
            return HttpResponseRedirect(reverse("teams:driver_page", kwargs={'id': id}))
        self.handle_invalid_form(request, id, form_sell=form)
        
        

class FireDriverView(LoginRequiredMixin, ManagerContextMixin, FormHandlingMixin, View):
    
    def post(self, request, id):
        form = FireDriverForm(request.POST)
        if form.is_valid():
            driver = Driver.objects.get(id=id)
            driver.terminate_contract()
            list_driver(id, 0)
            return HttpResponseRedirect(reverse("teams:driver_page", kwargs={'id': id}))
        self.handle_invalid_form(request, id, form_fire=form)
        return HttpResponseRedirect(reverse("manager:index"))
    

class BidDriverView(LoginRequiredMixin, ManagerContextMixin, FormHandlingMixin, View):

    def post(self, request, id):
        context = super().get_context_data()
        bidder = Team.objects.get(manager=context["current_user_manager"])
        form = DriverBidForm(bidder=bidder, data=request.POST)
        if form.is_valid():
            dl = form.cleaned_data["driver_listing"]
            if dl.active():
                bid_driver(id, bidder, form.cleaned_data["amount"])
                return HttpResponseRedirect(reverse("teams:driver_page", kwargs={'id': id}))
            sell_driver(id, form.cleaned_data["driver_listing"])
        return self.handle_invalid_form(request, id, form_bid=form)
       
