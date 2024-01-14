from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView, ContextMixin
from django.urls import reverse

from registration.helpers import create_manager_model
from manager.models import Manager, Team, Racetrack, Country


class ManagerContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manager = self.request.user.manager
        unread_messages = manager.unread_messages()
        context['current_user_manager'] = manager
        context['unread_messages'] = unread_messages
        return context
    

class IndexView(View):
    template_name = "manager/index.html"

    def get(self, request):
        manager = None
        unread_messages = False
        if request.user.is_authenticated:
            try:
                manager = Manager.objects.get(user=request.user)
                unread_messages = manager.unread_messages()
                Team.objects.get(owner=manager)
            except Manager.DoesNotExist:
                create_manager_model(request.user)
            except Team.DoesNotExist:
                return HttpResponseRedirect(reverse("teams:create_team"))
        return render(request, self.template_name, {
            "current_user_manager": manager,
            "unread_messages": unread_messages,
        })
    

class ManualView(TemplateView):
    template_name = "manager/manual.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manager = self.request.user.manager
        context['current_user_manager'] = manager
        return context



    