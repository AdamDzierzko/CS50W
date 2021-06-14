from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("category/<str:categoryName>", views.category, name="category"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("addToWatchlist/<int:listing_id>", views.addToWatchlist, name="addToWatchlist"),
    path("removeFromWatchlist/<int:listing_id>", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("one/<int:id>", views.one, name="one"),
    path("riseBid/<int:listing_id>",views.riseBid, name="riseBid"),
    path("addComment/<int:listing_id>", views.addComment, name="addComment"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("winns", views.winns, name="winns"),
    path("my", views.my, name="my")
]