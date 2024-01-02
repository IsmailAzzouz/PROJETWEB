# views.py
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import HttpResponse, get_object_or_404

from users.models import Profile
from .forms import GameForm, JoinGameForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET, require_POST

from .models import Game, Cell, Grid
from .models import Cell

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
            title = request.POST.get('game_title')

            if grid_x and (int(grid_x) < 3 or int(grid_x) > 12):
                errors['grid_x'] = 'Grid X must be between 3 and 12.'

            if grid_y and (int(grid_y) < 3 or int(grid_y) > 12):
                errors['grid_y'] = 'Grid Y must be between 3 and 12.'

            if alignment and (int(alignment) > max(int(grid_x), int(grid_y)) or int(alignment) < 3):
                errors['alignment'] = 'Alignment should be between 3 and X/Y.'
            if title is None or title == "":
                errors['title'] = "Game Title is a required field & must less or equal to 128 characters"

            if not errors:
                # Create and save the Game instance
                game = form.save(commit=False)
                game.player_1 = request.user
                game.player_2 = None
                game.nextplayer = request.user
                game.game_title = title
                game.save()

                request.session['game_code'] = game.id_code

                # Redirect to a success page or any other appropriate action
                return JsonResponse({'success': True, 'redirect': 'waiting-page'})
            else:
                # Return JSON data for custom errors
                print(errors)
                return JsonResponse({'success': False, 'errors': errors})
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

            if game.player_2 and (
                    request.user == game.player_1 or request.user == game.player_2) and game.isfinished is False:
                return JsonResponse({'success': True})

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
                if game.isfinished:
                    return JsonResponse({'success': False, 'message': 'Game is already finished'})
                else:

                    return JsonResponse({'success': False, 'message': 'Game is already full'})

        except Game.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Game not found'})
    else:
        return JsonResponse({'success': False, 'message': 'Please enter a code'})


def waiting_page(request):
    return render(request, 'WaitingforPlayer.html', context={'idcode': request.session['game_code']})


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
    player_1_username = game.player_1.username
    player_2_username = game.player_2.username
    current_user_role = 'Player 1' if request.user.username == player_1_username else 'Player 2'
    player1_symbol_mapping = {
        "Lila": "/media/PlayersIcon/LILA/LILA_CROSS_ICON.PNG",
        "Neon": "/media/PlayersIcon/NEON/NEON_CROSS_ICON.PNG",
        "3Dshaped": "/media/PlayersIcon/3DSHAPED/3DSHAPED_CROSS_ICON.PNG",
        "Green": "/media/PlayersIcon/GREEN/GREEN_CROSS_ICON.PNG",
        "Pastel": "media/PlayersIcon/PASTEL/PASTEL_CROSS_ICON.PNG",
    }
    player2_symbol_mapping = {
        "Lila": "/media/PlayersIcon/LILA/LILA_CIRCLE_ICON.PNG",
        "Neon": "/media/PlayersIcon/NEON/NEON_CIRCLE_ICON.PNG",
        "3Dshaped": "/media/PlayersIcon/3DSHAPED/3DSHAPED_CIRCLE_ICON.PNG",
        "Green": "/media/PlayersIcon/GREEN/GREEN_CIRCLE_ICON.PNG",
        "Pastel": "media/PlayersIcon/PASTEL/PASTEL_CIRCLE_ICON.PNG",
    }

    player_1_symbol = player1_symbol_mapping.get(game.player_1.profile.user_symbol, "")
    player_2_symbol = player2_symbol_mapping.get(game.player_2.profile.user_symbol, "")

    return render(request, 'GameScene.html', {
        'player_1': player_1_username,
        'player_2': player_2_username,
        'game_idcode': game_idcode,
        'game_private': game_private,
        'game_x': game_x,
        'game_y': game_y,
        'current_user_role': current_user_role,
        'alignement': game_alignment,
        'player_1_symbol': player_1_symbol,
        'player_2_symbol': player_2_symbol,
        'gametitle':game.game_title,
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
        {'code': game.id_code, 'grid_X': game.grid_x, 'grid_Y': game.grid_y, 'alignement': game.alignment,
         'title': game.game_title, } for game in
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
        cell.value = symbol
        print("symbol :", symbol + "\n row : ", row, "\n col : ", col)
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


def getnextplayerturn(request, game_idcode):
    game = get_object_or_404(Game, id_code=game_idcode)
    if request.user == game.player_1:
        game.nextplayer = game.player_2
        game.save()
        nextplayer = game.nextplayer.username
        print(nextplayer)
        return JsonResponse({'nextplayer': nextplayer})
    else:
        game.nextplayer = game.player_1
        game.save()
        nextplayer = game.nextplayer.username
        print(nextplayer)
        return JsonResponse({'nextplayer': nextplayer})


def checkturn(request, game_idcode):
    game = get_object_or_404(Game, id_code=game_idcode)
    nextplayer = game.nextplayer.username
    return JsonResponse({'nextplayer': nextplayer})


def setwinner(request, game_idcode):
    game = get_object_or_404(Game, id_code=game_idcode)
    game.winner = game.nextplayer
    game.isfinished = True
    if game.nextplayer is game.player_1:
        cells = Cell.objects.filter(grid=game.grid, value="0").count()

    else:
        cells = Cell.objects.filter(grid=game.grid, value="1").count()
    winner = game.nextplayer
    winner.profile.user_score = winner.profile.user_score + ((100 / cells) * 10)
    winner.save()
    game.save()
    game.player_1.save()
    game.player_2.save()
    playerwinner = game.winner
    message = f'{playerwinner.username} Has Won the GAME !'
    return JsonResponse({'message': message})


def checkwinner(request, game_idcode):
    game = get_object_or_404(Game, id_code=game_idcode)

    if game.winner == None:
        winner = "none"
    else:
        winner = game.winner.username

    return JsonResponse({'winner': winner})


def setdraw(request, game_idcode):
    game = get_object_or_404(Game, id_code=game_idcode)
    game.isfinished = True
    game.save()
    return JsonResponse({'message': 'game saved succefully'})


def surrender(request, game_idcode):
    try:
        playername = request.POST.get('playername', '')
        game = get_object_or_404(Game, id_code=game_idcode)
        game.player_2.profile.user_gameplayed += 1
        game.player_1.profile.user_gameplayed += 1

        if game.player_1.username == playername:
            game.winner = game.player_2

        else:
            game.winner = game.player_1

        game.isfinished = True
        game.has_surrendered = True
        game.save()
        game.winner.profile.user_game_won += 1
        game.player_1.save()
        game.player_2.save()
        print(playername)
        return JsonResponse({'message': 'game saved successfully'})

    except Exception as e:
        return JsonResponse({'error': str(e)})


def scoreboard(request):
    users = Profile.objects.all().order_by('user_rank')

    # Calculate ratio for each user
    for user in users:
        if user.user_gameplayed != 0:
            user.ratio = user.user_game_won / user.user_gameplayed
        else:
            user.ratio = 0  # Set a default value if user has not played any games

    context = {
        'users': users,
    }
    return render(request, "ScoreBoard.html", context)
