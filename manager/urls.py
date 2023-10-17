from django.urls import include, path

from manager.views.generic import IndexView

app_name = "manager"


generic_patterns = [
    path("", IndexView.as_view(), name="index"),
]


urlpatterns = [
    path("", include(generic_patterns)),
    path("accounts/", include("django.contrib.auth.urls")),
]
