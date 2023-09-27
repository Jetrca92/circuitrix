from django.urls import include, path

from .views import generic

generic_patterns = [
    path("", generic.index, name="index"),
]

urlpatterns = [
    path("", include(generic_patterns)),
]
