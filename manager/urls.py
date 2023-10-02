from django.urls import include, path

from .views import generic

app_name = "manager"


generic_patterns = [
    path("", generic.index, name="index"),
]

urlpatterns = [
    path("", include(generic_patterns)),
    path("accounts/", include("django.contrib.auth.urls")),
]
