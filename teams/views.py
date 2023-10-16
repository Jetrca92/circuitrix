from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse

from teams.forms import NewTeamForm
from manager.models import Manager, Team, Country
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
        if form.is_valid():
            team_name = form.cleaned_data["team_name"]
            team_country = form.cleaned_data["team_country"]
            manager = Manager.objects.get(user=request.user)
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
