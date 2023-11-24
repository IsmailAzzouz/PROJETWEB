# views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import HttpResponse, get_object_or_404
from .forms import GameForm, JoinGameForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST
from PROJETWEB import urls

from .models import Game, Cell, Grid

from django.http import JsonResponse


def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            # Create a new Game instance
            errors = {}
            grid_x = request.POST.get('grid_x')
            grid_y = request.POST.get('grid_y')
            alignment = request.POST.get('alignment')

            if grid_x and (int(grid_x) < 3 or int(grid_x) > 12):
                errors['grid_x'] = 'Grid X must be between 3 and 12.'

            if grid_y and (int(grid_y) < 3 or int(grid_y) > 12):
                errors['grid_y'] = 'Grid Y must be between 3 and 12.'

            if alignment and (int(alignment) > max(int(grid_x), int(grid_y)) or int(alignment) < 3):
                errors['alignment'] = 'Alignment should be between 3 and X/Y.'

            if not errors:
                # Create and save the Game instance
                game = form.save(commit=False)
                game.player_1 = request.user
                game.player_2 = None
                game.save()

                request.session['game_code'] = game.id_code

                # Redirect to a success page or any other appropriate action
                return JsonResponse({'success': True, 'redirect': 'waiting-page'})
            else:
                # Return JSON data for custom errors
                print(errors)
                return JsonResponse({'success': False, 'errors': errors}, status=400)
        else:
            # Return JSON data for form errors

            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
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
            return JsonResponse({'success': False, 'message': 'Game not found'})
    else:
        return JsonResponse({'success': False, 'message': 'Please enter a code'}) #if return status 404 can't get the message form the json response and show an error in console


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


# views.py


import json


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


def handle_player_move(request, game_id):
    if request.method == 'POST':
        row = int(request.POST.get('row'))
        col = int(request.POST.get('col'))
        player = int(request.POST.get('player'))

        # Look up the game in the database based on game_id
        game = get_object_or_404(Game, id=game_id)

        # Check if it's the correct player's turn
        if game.current_player != player:
            return JsonResponse({'validMove': False, 'error': 'It\'s not your turn.'})

        # Check if the cell is empty
        if game.board[row][col] != '':
            return JsonResponse({'validMove': False, 'error': 'Cell already taken.'})

        # Update the game state (this is a simplified example)
        game.board[row][col] = 'X' if player == 1 else 'O'
        game.current_player = 3 - player  # Toggle between 1 and 2

        # Check for a winner or draw (you need to implement this logic based on your game rules)
        winner = check_winner(game.board)
        draw = check_draw(game.board)

        game.save()

        return JsonResponse({'validMove': True, 'winner': winner, 'draw': draw})
    else:
        return JsonResponse({'validMove': False, 'error': 'Invalid request method'})


def check_winner(board):
    # Check rows
    for row in board:
        if all(cell == row[0] and cell != '' for cell in row):
            return int(row[0])  # Player number who won

    # Check columns
    for col in range(len(board[0])):
        if all(row[col] == board[0][col] and board[0][col] != '' for row in board):
            return int(board[0][col])  # Player number who won

    # Check diagonals
    if all(board[i][i] == board[0][0] and board[0][0] != '' for i in range(len(board))):
        return int(board[0][0])  # Player number who won

    if all(board[i][len(board) - 1 - i] == board[0][len(board) - 1] and board[0][len(board) - 1] != '' for i in
           range(len(board))):
        return int(board[0][len(board) - 1])  # Player number who won

    return None  # No winner


def check_draw(board):
    # Check if there are any empty cells left
    return all(cell != '' for row in board for cell in row)


def play(request):
    return render(request, 'Play.html')


def generategametable(request):
    # Récupérer les données du tableau de scores
    games = Game.objects.filter(player_2__isnull=True, private=False)

    # Convertir le QuerySet en une liste de dictionnaires
    scoreboard_data = [
        {'code': game.id_code, 'grid_X': game.grid_x, 'grid_Y': game.grid_y, 'alignement': game.alignment, } for game in
        games]

    return JsonResponse(scoreboard_data, safe=False)


def update_cell_in_database(request, game_idcode):
    if request.method == 'POST':
        row = int(request.POST.get('row'))
        col = int(request.POST.get('col'))
        symbol = request.POST.get('symbol')

        # Get the game object
        game = get_object_or_404(Game, id_code=game_idcode)

        # Get the grid associated with the game
        grid = get_object_or_404(Grid, game=game)

        # Get the cell associated with the grid, row, and col
        cell = get_object_or_404(Cell, grid=grid, x_position=row, y_position=col)

        # Update the corresponding cell in the database
        cell.value = 1
        cell.save()

        return HttpResponse(status=200)

    return HttpResponse(status=400)


def getCellValueFromDatabase(request, game_idcode):
    try:
        row = int(request.POST.get('row', 0))
        col = int(request.POST.get('col', 0))
    except ValueError:
        return HttpResponseBadRequest('Invalid row or col value.')

    game = get_object_or_404(Game, id_code=game_idcode)
    grid = get_object_or_404(Grid, game=game)
    cell = get_object_or_404(Cell, grid=grid, x_position=row, y_position=col)

    return JsonResponse({'cellValue': cell.value})
