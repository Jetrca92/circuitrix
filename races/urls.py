from django.urls import path

from races.views import ChampionshipOverviewView

app_name = "races"

urlpatterns = [
    path("<int:id>/overview", ChampionshipOverviewView.as_view(), name="championship_overview"),
    
    
]