from django.urls import include, path

from teams.views import CreateTeamView, TeamOverviewView, DriversView

app_name = "teams"

urlpatterns = [
    path("create_team", CreateTeamView.as_view(), name="create_team"),
    path("<int:id>/overview", TeamOverviewView.as_view(), name="team_overview"),
    path("<int:id>/drivers", DriversView.as_view(), name="drivers"),
]
