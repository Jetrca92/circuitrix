from django.urls import include, path

from teams.views import CreateTeamView

app_name = "teams"

urlpatterns = [
    path("create_team", CreateTeamView.as_view(), name="create_team"),
]
