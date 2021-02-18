from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.category, name="category"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watch/<int:id>", views.watch, name="watch"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close/<int:id>", views.close, name="close"),
    path("comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]

