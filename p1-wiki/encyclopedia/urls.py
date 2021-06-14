from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
	path("wiki/<str:entryName>", views.readEntry, name="entry"),
    path("search", views.searchEntry, name="search"),
    path("newPage", views.newPage, name="newPage"),
    path("randomPage", views.randomPage, name="randomPage"),
    path("editPage/<str:entryName>", views.editPage, name="editPage")
]
