# forms.py
from django import forms
from .models import Game


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['private', 'grid_x', 'grid_y', 'alignment', 'game_title']


class JoinGameForm(forms.Form):
    game_code = forms.CharField(max_length=11)
