from django.urls import path

from races.views import ChampionshipOverviewView, RacetrackView, RacetracksOverviewView, RacesOverviewView, RaceView

app_name = "races"

urlpatterns = [
    path("<int:id>/overview", ChampionshipOverviewView.as_view(), name="championship_overview"),
    path("racetrack/<int:id>", RacetrackView.as_view(), name="racetrack"),
    path("<int:id>/racetracks", RacetracksOverviewView.as_view(), name="racetracks_overview"),
    path("race/<int:id>", RaceView.as_view(), name="race"),
    path("<int:id>/races", RacesOverviewView.as_view(), name="races_overview"),
    
]