from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from Game.models import Game
from HelbMorpion.forms import CommunityMessageForm


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
    context = {"message": message, }
    return render(request, 'index.html', context, )


def about(request):
    return render(request, 'About.html')
def succespage(request):
    return render(request, 'succesmessage.html')

def contact_view(request):
    if request.method == 'POST':
        form = CommunityMessageForm(request.POST)
        if form.is_valid():
            form.save()
            # You can add additional logic here, like sending an email or showing a success message.
            return redirect('success_page')  # Replace 'success_page' with the actual success page name or URL.
    else:
        form = CommunityMessageForm()

    return render(request, 'contact.html', {'form': form})
