from django.urls import path
from . import views

urlpatterns = [

    # HTML Pages
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("change-password/", views.change_password, name="change_password"),

    # REST API
    path("api/login/", views.api_login),
    path("api/register/", views.register),
    path("api/profile/", views.profile),
    path("api/change-password/", views.change_password),
    path("api/update-profile/", views.update_profile),


]