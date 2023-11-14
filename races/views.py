from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from django.views.generic.base import ContextMixin

from manager.models import Championship, Race, Racetrack


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
    

class RacetrackView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Racetrack
    template_name = "races/racetrack.html"
    context_object_name = "racetrack"

    def get_object(self, queryset=None):
        racetrack = Racetrack.objects.get(pk=self.kwargs['id']  )
        return racetrack
    

class RacetracksOverviewView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Championship
    template_name = "races/racetracks_overview.html"
    context_object_name = "championship"

    def get_object(self, queryset=None):
        championship = Championship.objects.get(pk=self.kwargs['id'])
        return championship
    

class RaceView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Race
    template_name = "races/race.html"
    context_object_name = "race"

    def get_object(self, queryset=None):
        race = Race.objects.get(pk=self.kwargs['id'])
        return race


class RacesOverviewView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Championship
    template_name = "races/races_overview.html"
    context_object_name = "championship"

    def get_object(self, queryset=None):
        championship = Championship.objects.get(pk=self.kwargs['id'])
        return championship

