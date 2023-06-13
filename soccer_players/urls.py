from django.urls import path
from . import views

urlpatterns = [
     path("", views.index, name="index"),
     path("teams/<int:num>", views.number, name="number"),
     path("teams/players/", views.players, name="players")
]