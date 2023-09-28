from django.urls import include, path

from .views import generic, auth


auth_patterns = [
    path("login", auth.login_view, name="login"),
    path("forgot-password", auth.forgot_password, name="forgot_password"),
    path("logout", auth.logout_view, name="logout"),
    path("register", auth.register, name="register"),
]


generic_patterns = [
    path("", generic.index, name="index"),
]

urlpatterns = [
    path("", include(generic_patterns)),
    path("auth/", include(auth_patterns)),
]
