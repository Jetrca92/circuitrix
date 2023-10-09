from django.urls import include, path

from manager.views import generic
from manager.views.generic import IndexView, CreateTeamView

app_name = "manager"


generic_patterns = [
    path("", IndexView.as_view(), name="index"),
    path("create_team", CreateTeamView.as_view(), name="create_team"),
]

urlpatterns = [
    path("", include(generic_patterns)),
    path("accounts/", include("django.contrib.auth.urls")),
]
