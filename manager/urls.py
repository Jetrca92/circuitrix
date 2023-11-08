from django.urls import include, path

from manager.views.generic import IndexView, ManualView

app_name = "manager"


generic_patterns = [
    path("", IndexView.as_view(), name="index"),
    path("manual", ManualView.as_view(), name="manual"),
]


urlpatterns = [
    path("", include(generic_patterns)),
    path("accounts/", include("django.contrib.auth.urls")),
]
