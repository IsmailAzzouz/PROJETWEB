# views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect

from .forms import GameForm, JoinGameForm
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from PROJETWEB import urls

from .models import Game


def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            # Create a new Game instance
            game = form.save(commit=False)

            # Set player_1 to the current user (the one who created the game)
            game.player_1 = request.user

            # Set player_2 to None initially
            game.player_2 = None

            # Save the game instance
            game.save()

            request.session['game_code'] = game.id_code

            # Redirect to a success page or any other appropriate action
            return JsonResponse({'success': True, 'redirect': 'waiting-page'})
        else:
            # Return JSON data for form errors
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    else:
        form = GameForm()

    return render(request, 'CreatingGame.html', {'form': form})


@require_GET
def check_game_status(request):
    # Assuming the game code is stored in the session
    game_code = request.session.get('game_code')

    if game_code:
        try:
            # Retrieve the game instance based on the game code
            game = Game.objects.get(id_code=game_code)
            player_1_connected = is_user_authenticated(game.player_1)

            # Check if both players are connected
            if game.player_2 is not None:
                player_2_connected = is_user_authenticated(game.player_2)
                if player_1_connected and player_2_connected:
                    # Include player data and game settings in the JSON response
                    response_data = {
                        'ready': True,
                        'player_1': game.player_1.username,
                        'player_2': game.player_2.username,
                        'game_idcode': game.id_code,
                        'game_private': game.private,
                        'other_game_data': 'your_additional_game_data',
                    }
                    return JsonResponse(response_data)
            else:
                # Respond with a JSON object indicating game status
                return JsonResponse({'ready': False})

        except Game.DoesNotExist:
            # Handle the case where the game with the given code does not exist
            return JsonResponse({'error': 'Game not found'}, status=404)

    # Handle the case where there is no game code in the session
    return JsonResponse({'error': 'Game code not found'}, status=400)


def is_user_authenticated(user):
    return user.is_authenticated


@require_POST
def join_game(request):
    form = JoinGameForm(request.POST)

    if form.is_valid():
        game_code = form.cleaned_data['game_code']

        try:
            game = Game.objects.get(id_code=game_code)

            if not game.player_2:
                # Fetch the User instance based on the username
                user_joining = User.objects.get(username=request.user.username)

                # Set player_2 to the User instance
                game.player_2 = user_joining
                game.save()

                # Store the game code in the session
                request.session['game_code'] = game_code
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Game is already full'})

        except Game.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Game not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid form data'}, status=400)


def waiting_page(request):
    return render(request, 'WaitingforPlayer.html')


def joining_page(request):
    return render(request, 'JoinGame.html')


def game_scene(request, player_1, player_2, game_idcode, game_private):
    # Look up the game in the database based on game_idcode
    game = get_object_or_404(Game, id_code=game_idcode)

    # You can now access additional settings from the game instance
    game_x = game.grid_x
    game_y = game.grid_y
    game_alignment = game.alignment

    return render(request, 'GameScene.html', {
        'player_1': player_1,
        'player_2': player_2,
        'game_idcode': game_idcode,
        'game_private': game_private,
        'game_x': game_x,
        'game_y': game_y,
        'game_alignment': game_alignment,
    })
