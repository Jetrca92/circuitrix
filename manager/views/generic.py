from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse

from registration.helpers import create_manager_model
from manager.models import Manager, Team


class IndexView(View):
    template_name = "manager/index.html"

    def get(self, request):
        manager = None
        if request.user.is_authenticated:
            try:
                manager = Manager.objects.get(user=request.user)
                team = Team.objects.get(owner=manager)
            except Manager.DoesNotExist:
                create_manager_model(request.user)
            except Team.DoesNotExist:
                return HttpResponseRedirect(reverse("teams:create_team"))
        return render(request, self.template_name, {
            "manager": manager,
        })
    


    