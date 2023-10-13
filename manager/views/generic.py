from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse

from manager.models import Manager, Team


class IndexView(View):
    template_name = "manager/index.html"

    def get(self, request):
        if request.user.is_authenticated:
            try:
                manager = Manager.objects.get(user=request.user)
                team = Team.objects.get(owner=manager)
            except Manager.DoesNotExist:
                # TO DO Handle if manager doesn't exist
                return render(self.request, self.template_name)
            except Team.DoesNotExist:
                return HttpResponseRedirect(reverse("teams:create_team"))
                # TO DO Handle if team doesn't exist
                return render(request, self.template_name)

        return render(request, self.template_name)
    


    