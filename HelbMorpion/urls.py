from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="morpion-home"),
    path("about/", views.about, name="morpion-about"),

]
