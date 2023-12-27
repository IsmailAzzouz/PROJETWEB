from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from Game.models import Game


# Create your views here.
def home(request):
    message = ""
    if 'game_code' in request.session and (
            request.session['game_code'] is not None and request.session['game_code'] != ""):

        try:
            game = Game.objects.get(id_code=request.session['game_code'])
            if game.has_surrendered:
                if game.winner == request.user:
                    message = "Your opponent surrendered That's why you've won the game!"

                else:
                    message = "You've surrendered your last game!"



        except Game.DoesNotExist:

            pass
    request.session['game_code'] = ""
    context = {"message": message,}
    return render(request, 'index.html', context,)

def about(request):
    return HttpResponse("<h1>about</h1>")