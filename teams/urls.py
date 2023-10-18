from django.urls import include, path

from teams.views import CreateTeamView, TeamOverviewView, DriversView, DriverPageView, TeamOwnerView, TeamStaffView, TeamCarView

app_name = "teams"

urlpatterns = [
    path("create_team", CreateTeamView.as_view(), name="create_team"),
    path("<int:id>/overview", TeamOverviewView.as_view(), name="team_overview"),
    path("<int:id>/drivers", DriversView.as_view(), name="drivers"),
    path("driver/<int:id>", DriverPageView.as_view(), name="driver_page"),
    path("<int:id>/owner", TeamOwnerView.as_view(), name="team_owner"),
    path("<int:id>/staff", TeamStaffView.as_view(), name="staff"),
    path("<int:id>/car", TeamCarView.as_view(), name="car"),
]
