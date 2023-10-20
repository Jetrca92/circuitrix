from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.base import ContextMixin
from django.urls import reverse

from teams.forms import NewTeamForm
from manager.models import Manager, Team, Country, Driver, LeadDesigner, RaceMechanic, Car
from teams.forms import NewTeamForm
from teams.helpers import (
    generate_car,
    generate_drivers,
    generate_lead_designer,
    generate_race_mechanics,
)


class ManagerContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manager = self.request.user.manager
        context['manager'] = manager
        return context
    

class CreateTeamView(LoginRequiredMixin, View):
    template_name = "teams/create_team.html"

    def get(self, request):
        user = request.user
        manager = Manager.objects.get(user=user)
        form = NewTeamForm()
        countries = Country.objects.all()
        context = {
            "countries": countries,
            "manager": manager,
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = NewTeamForm(request.POST)
        countries = Country.objects.all()
        manager = Manager.objects.get(user=request.user)
        if form.is_valid():
            team_name = form.cleaned_data["team_name"]
            team_country = form.cleaned_data["team_country"]
            team_country_object = Country.objects.get(id=int(team_country))
            try:
                with transaction.atomic():
                    # Create team and generate staff and facilities
                    team = Team(name=team_name, location=team_country_object, owner=manager)
                    team.save()
                    generate_drivers(team)
                    generate_lead_designer(team)
                    generate_race_mechanics(team)
                    generate_car(team)
                    team.save()
                    manager.team = team
                    manager.save()
                    return HttpResponseRedirect(reverse("manager:index"))
            except IntegrityError:
                return render(request, self.template_name, {
                    "message": "Integrity Error!"
                })
        else:
            return render(request, self.template_name, {
                "form": form,
                "manager": manager,
                "countries": countries,
            })
    

class TeamOverviewView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Team
    template_name = "teams/team_overview.html"
    context_object_name = "team"

    def get_object(self, queryset=None):
        team = Team.objects.get(pk=self.kwargs['id']  )
        return team
    

class DriversView(LoginRequiredMixin, ManagerContextMixin, ListView):
    model = Driver
    template_name="teams/drivers.html"
    context_object_name = "drivers"

    def get_queryset(self):
        team = Team.objects.get(pk=self.kwargs['id'])
        return team.drivers.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.get(pk=self.kwargs['id'])
        context['team'] = team
        return context
    

class DriverPageView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Driver
    template_name = "teams/driver_page.html"
    context_object_name = "driver"

    def get_object(self, queryset=None):
        driver = Driver.objects.get(pk=self.kwargs['id'])  
        return driver
    

class TeamOwnerView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Manager
    template_name = "teams/team_owner.html"
    context_object_name = "owner"

    def get_object(self, queryset=None):
        team = Team.objects.get(pk=self.kwargs['id'])
        return team.owner


class TeamStaffView(LoginRequiredMixin, ManagerContextMixin, ListView):
    model = RaceMechanic
    template_name = "teams/staff.html"
    context_object_name = "race_mechanics"

    def get_queryset(self):
        team = Team.objects.get(pk=self.kwargs['id'])
        return team.race_mechanics.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.get(pk=self.kwargs['id'])
        context['team'] = team
        return context
    

class TeamCarView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Car
    template_name = "teams/car.html"
    context_object_name = "car"

    def get_object(self, queryset=None):
        team = Team.objects.get(pk=self.kwargs['id'])
        return team.car
