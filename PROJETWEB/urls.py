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

from HelbMorpion.views import contact_view, succespage
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from Game.views import *
from users.views import filter_games, change_user_symbol

urlpatterns = [
                  path('', include('HelbMorpion.urls')),
                  path('contact/', contact_view, name='contact_page'),
                  path('succes/', succespage, name='success_page'),
                  path('admin/', admin.site.urls),
                  path('statistics/', statistics, name='statistics'),
                  path('register/', user_views.register, name='register'),
                  path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
                  path('profile/', user_views.profile, name='profile'),
                  path('profile/filtergames', filter_games, name='filtergames'),
                  path('profile/change_user_symbol', change_user_symbol, name='change_user_symbol'),
                  path('create_game/', create_game, name='create_game'),
                  path('scoreboard/', scoreboard, name='scoreboard'),
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
                  path('Play/', play,
                       name="Play"),
                  path('gametable/', generategametable, name='GameTable'),
                  path('gamescene/move/', handle_player_move, name='handle_player_move'),
                  path('gamescene/move/update_cell_in_database/<str:game_idcode>/', update_cell_in_database,
                       name='update_cell_in_database'),
                  path('gamescene/move/get_cell_value_from_database/<str:game_idcode>/', getCellValueFromDatabase,
                       name='get_cell_value_from_database'),
                  path('gamescene/move/getplayerturn/<str:game_idcode>/', getnextplayerturn, name='getnextplayerturn'),
                  path('gamescene/move/checkturn/<str:game_idcode>/', checkturn, name='checkturn'),
                  path('gamescene/move/checkwinner/<str:game_idcode>/', checkwinner, name='checkwinner'),
                  path('gamescene/move/setwinner/<str:game_idcode>/', setwinner, name='setwinner'),
                  path('gamescene/move/setdraw/<str:game_idcode>/', setdraw, name='setdraw'),
                  path('gamescene/move/surrender/<str:game_idcode>/', surrender, name='surrender'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
