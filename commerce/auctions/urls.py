from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("closed", views.closed, name="closed"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("commenting/<int:id>", views.commenting, name="commenting"),
    path("list/<int:id>", views.list, name="list"),
    path("bid/<int:id>", views.newbid, name="newbid"), 
    path("closing/<int:id>", views.closing, name="closing"),
    path("closinglist/<int:id>", views.closinglist, name="closinglist"),
    path("watchlistsave/<int:id>", views.watchlist_save, name="watchlistsave"),
    path("watchlistremove/<int:id>", views.watchlist_remove, name="watchlistremove"),
    path("list/<str:cat>", views.sort, name="sort"),
    ]
