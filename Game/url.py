from django.urls import path
from . import views

urlpatterns = [
    path('CreateGame', views.Game, name="CreatingGame"),
    path("waiting", views.check_game_status, name="Wainting"),

]
