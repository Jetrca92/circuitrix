from django.urls import path

from races.views import ChampionshipOverviewView, RacetrackView, RacetracksOverviewView

app_name = "races"

urlpatterns = [
    path("<int:id>/overview", ChampionshipOverviewView.as_view(), name="championship_overview"),
    path("racetrack/<int:id>", RacetrackView.as_view(), name="racetrack"),
    path("<int:id>/racetracks", RacetracksOverviewView.as_view(), name="racetracks_overview"),
    
    
]