from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse

from races.constants import racetracks
from races.helpers import create_racetracks, create_countries
from registration.helpers import create_manager_model
from manager.models import Manager, Team, Racetrack, Country
from teams.constants import countries


class IndexView(View):
    template_name = "manager/index.html"

    def get(self, request):
        manager = None
        if not Country.objects.exists():
            create_countries(countries)
        if not Racetrack.objects.exists():
            create_racetracks(racetracks)
        


        if request.user.is_authenticated:
            try:
                manager = Manager.objects.get(user=request.user)
                Team.objects.get(owner=manager)
            except Manager.DoesNotExist:
                create_manager_model(request.user)
            except Team.DoesNotExist:
                return HttpResponseRedirect(reverse("teams:create_team"))
        return render(request, self.template_name, {
            "current_user_manager": manager,
        })
    


    