"""
URL configuration for PROJETWEB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from Game.views import *

urlpatterns = [
                  path('', include('HelbMorpion.urls')),
                  path('admin/', admin.site.urls),
                  path('register/', user_views.register, name='register'),
                  path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
                  path('profile/', user_views.profile, name='profile'),
                  path('create_game/', create_game, name='create_game'),
                  path('waiting/', waiting_page,
                       name="waiting-page"),
                  path('waiting/checkgamestatus/', check_game_status,
                       name="checking-page"),
                  path('joingame/', joining_page,
                       name="joining-page"),
                  path('joining/', join_game,
                       name="join-game"),
                  path(
                      'gamescene/gamecreator=<str:player_1>/player2=<str:player_2>/gamecode=<str:game_idcode>/isgameprivate=<str:game_private>/',
                      game_scene, name='Game-Scene'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
