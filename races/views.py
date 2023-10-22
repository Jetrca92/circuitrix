from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.base import ContextMixin

from manager.models import  Team, Championship, Race


class ManagerContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manager = self.request.user.manager
        context['current_user_manager'] = manager
        return context
    

class ChampionshipOverviewView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Championship
    template_name = "races/championship_overview.html"
    context_object_name = "championship"

    def get_object(self, queryset=None):
        championship = Championship.objects.get(pk=self.kwargs['id']  )
        return championship
    
