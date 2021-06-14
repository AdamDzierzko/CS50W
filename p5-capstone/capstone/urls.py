from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("allmovies", views.index, name="allmovies"),
    path("best", views.best, name="best"),
    path("mostpopular", views.mostpopular, name="mostpopular"),
    path("addmovie", views.addmovie, name="addmovie"),
    path("delete_movie/<int:movie_id>", views.delete_movie, name="delete_movie"),
    path("edit_movie/<int:movie_id>", views.edit_movie, name="edit_movie"),

    path("config", views.config, name="config"),
    path("addgenere", views.addgenere, name="addgenere"),
    path("addactor", views.addactor, name="addactor"),

    path("addgrade", views.addgrade, name="addgrade"),
    path("edit_grade/<int:grade_id>", views.edit_grade, name="edit_grade"),
    path("edit_grade_com/<int:movie_id>", views.edit_grade_com, name="edit_grade_com"),

    path("coment_index/<int:movie_id>", views.coment_index, name="coment_index"),
    path("addcoment", views.addcoment, name="addcoment"),
    path("delete_coment/<int:coment_id>", views.delete_coment, name="delete_coment"),
    path("edit_coment/<int:coment_id>", views.edit_coment, name="edit_coment"),
]