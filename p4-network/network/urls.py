
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("add", views.add, name="add"),
    path("profil/<int:id>", views.profil, name="profil"),
    path("following", views.following, name="following"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:id>", views.like, name="like"),
    path("dislike/<int:id>", views.dislike, name="dislike"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("unfollow/<int:id>", views.unfollow, name="unfollow"),
]
