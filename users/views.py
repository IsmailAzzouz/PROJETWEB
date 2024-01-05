from datetime import timedelta, datetime

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from Game.models import Game

from django.contrib.auth import authenticate, login
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            user = form.save()


            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)

            messages.success(request, f'Account created successfully. You are now logged in.')
            return redirect('profile')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    games = Game.objects.all()
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Account Updated')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    filtered_games = Game.objects.filter(
        (Q(player_1__username=request.user.username) | Q(player_2__username=request.user.username)),
        isfinished=True,
    )
    last_3_games_data = [
        {
            'id_code': last_game.id_code,
            'grid_x': last_game.grid_x,
            'grid_y': last_game.grid_y,
            'player_1': last_game.player_1,
            'player_2': last_game.player_2,
            'alignement': last_game.alignment,
            'winner': getattr(last_game.winner, 'username', None),
            'game_date': last_game.game_date.strftime('%Y-%m-%d'),
        }
        for last_game in filtered_games[:3]
    ]
    user_username = request.user.username
    one_week_ago = datetime.now() - timedelta(weeks=1)

    filtered_games = Game.objects.filter(
        (Q(player_1__username=user_username) | Q(player_2__username=user_username)),
        isfinished=True,
        game_date__gte=one_week_ago,  # Filter games played in the last week
    )

    # You can customize this response based on your needs
    games_data = [
        {
            'id_code': game.id_code,
            'grid_x': game.grid_x,
            'grid_y': game.grid_y,
            'winner': getattr(game.winner, 'username', "None"),
            'game_date': game.game_date.strftime('%Y-%m-%d'),
        }
        for game in filtered_games
    ]
    if request.user.profile.user_gameplayed > 0:
        user_ratio = request.user.profile.user_game_won / request.user.profile.user_gameplayed
    else:
        user_ratio = 0
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'Games': games,
        'last_3_games': last_3_games_data,
        'all_player_games': games_data,
        'ratio': user_ratio,
    }

    return render(request, 'users/profile.html', context, )


@csrf_exempt  # Only for demonstration purposes, use proper CSRF protection in production
def filter_games(request):
    print("tes")
    if request.method == 'POST':
        try:
            x = int(request.POST.get('x'))
            y = int(request.POST.get('y'))
            alignement = int(request.POST.get('Alignement'))
            user_username = request.user.username
            print("X", x, "Y", y, 'User', user_username, "Aligne", alignement)
            # Filter games based on x, y, and user as winner
            filtered_games = Game.objects.filter(
                grid_x=x,
                grid_y=y,
                alignment=alignement,
                isfinished=True,
            )


            games_data = [
                {
                    'id_code': game.id_code,
                    'grid_x': game.grid_x,
                    'grid_y': game.grid_y,
                    'winner': getattr(game.winner, 'username', None),
                    'game_date': game.game_date.strftime('%Y-%m-%d'),
                    #'winner_image': game.winner.profile.image.path,
                }
                for game in filtered_games
            ]
            #print(games_data)
            return JsonResponse({'success': True, 'games': games_data})
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid parameters'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt  # Only for demonstration purposes, use proper CSRF protection in production
def change_user_symbol(request):
    if request.method == 'POST':
        try:
            print(request.POST.get('symbol'))
            user = request.user
            user.profile.user_symbol = request.POST.get('symbol')
            user.save()
            return JsonResponse({'success': True, })
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Invalid parameters'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
