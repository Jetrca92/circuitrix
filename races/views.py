from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.base import ContextMixin
from django.utils import timezone
from django.urls import reverse

from manager.models import Championship, Race, Racetrack, RaceResult, RaceOrders
from manager.views.generic import ManagerContextMixin
from races.helpers import get_race_drivers, calculate_race_result
    

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

    def get(self, request, *args, **kwargs):
        race = self.get_object()
        if race.date < timezone.now():
            results = RaceResult.objects.filter(race=race).first()
            if results is None:
                calculate_race_result(race)      
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        race = Race.objects.get(pk=self.kwargs['id'])
        return race
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        race = Race.objects.get(pk=self.kwargs['id'])
        race_results = race.results.all()
        context['race_results'] = race_results
        return context


class RacesOverviewView(LoginRequiredMixin, ManagerContextMixin, DetailView):
    model = Championship
    template_name = "races/races_overview.html"
    context_object_name = "championship"

    def get_object(self, queryset=None):
        championship = Championship.objects.get(pk=self.kwargs['id'])
        return championship
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        championship = Championship.objects.get(pk=self.kwargs['id'])
        context['upcoming_races'] = championship.upcoming_races()
        context['completed_races'] = championship.completed_races()
        context['ongoing_races'] = championship.ongoing_races()
        return context

