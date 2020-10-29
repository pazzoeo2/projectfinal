from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("view", views.view, name="view"),
    path("entry/<int:entryid>", views.entry, name="entry"),
    path("add", views.add, name="add"),
    path("searchquery", views.searchquery, name="searchquery"),
    path("addgame", views.addgame, name="addgame"),
    path("delete", views.delete, name="delete"),
    path("editentry", views.editentry, name="editentry"),
    path("addhours", views.addhours, name="addhours")
]
