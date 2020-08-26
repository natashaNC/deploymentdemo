from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path("register", views.register),
    path("home", views.home),
    path("login", views.login),
    path("logout", views.logout),
    path("addPost", views.addpost),
    path("createRant", views.createRant),
    path("like/<int:rantId>", views.likeRant),
    path("rants/<int:rantId>", views.showRant),
    path("unlike/<int:rantId>", views.unlikeRant)
]