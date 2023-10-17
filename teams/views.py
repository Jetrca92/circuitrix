from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from django.urls import reverse

from teams.forms import NewTeamForm
from manager.models import Manager, Team, Country, Driver
from teams.forms import NewTeamForm
from teams.helpers import (
    generate_car,
    generate_drivers,
    generate_lead_designer,
    generate_race_mechanics,
)


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


class TeamOverviewView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = "teams/team_overview.html"
    context_object_name = "team"

    def get_object(self, queryset=None):
        team_id = self.kwargs['id']  # Retrieve the team ID from the URL
        return Team.objects.get(pk=team_id)
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            manager = self.request.user.manager
            context['manager'] = manager
            return context
    

class DriversView(LoginRequiredMixin, ListView):
    model = Driver
    template_name="teams/drivers.html"
    context_object_name = "drivers"

    def get_queryset(self):
        team = Team.objects.get(pk=self.kwargs['id'])
        return team.drivers.all()

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            manager = self.request.user.manager
            context['manager'] = manager
            return context