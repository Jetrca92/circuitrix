from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse

from teams.forms import NewTeamForm
from manager.models import Manager, Team, Country
from teams.helpers import (
    generate_car,
    generate_drivers,
    generate_lead_designer,
    generate_race_mechanics,
)


class CreateTeamView(LoginRequiredMixin, View):
    
    def get(self, request):
        user = request.user
        manager = Manager.objects.get(user=user)
        form = NewTeamForm()
        try:
            countries = Country.objects.all()
        except Country.DoesNotExist:
            return self.render_error(request, "No Countries availdable!")
        context = {
            "countries": countries,
            "manager": manager,
            "form": form,
        }
        return render(request, "manager/create_team.html", context)

    def post(self, request):
        team_name = request.POST.get("team_name")
        team_country = int(request.POST.get("team_country"))
        manager = Manager.objects.get(user=request.user)

        if not team_name:
            return self.render_error(self.request, "Team name is required!")

        if Team.objects.filter(name=team_name).exists():
            return self.render_error(self.request, "Team name already exists!")

        if team_country == "selected":
            return self.render_error(self.request, "Select a country!")

        team_country_object = Country.objects.get(id=team_country)

        # Create team and generate staff and facilities
        team = Team(name=team_name, location=team_country_object, owner=manager)
        team.save()
        generate_drivers(team)
        generate_lead_designer(team)
        generate_race_mechanics(team)
        generate_car(team)
        team.save()
        
        return HttpResponseRedirect(reverse("manager:index"))

    def render_error(self, request, message):
        form = NewTeamForm()
        countries = Country.objects.all()
        return render(request, "manager/create_team.html", {"message": message, "countries": countries, "form": form})