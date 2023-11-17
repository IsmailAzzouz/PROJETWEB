from django.db import models
import random
import string
from django.contrib.auth.models import User


def generate_random_code():
    """Generate a random code consisting of 5 letters and 5 numbers."""
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f'{code[:5]}-{code[5:]}'


class Game(models.Model):
    id_code = models.CharField(max_length=11, default=generate_random_code, unique=True)
    X_parameter = models.IntegerField()
    Y_parameter = models.IntegerField()
    Player_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player_1_games")
    Player_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player_2_games")
    Private = models.BooleanField(default=False)
    Winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner_games")
    Alignment = models.IntegerField()

    def __str__(self):
        return f"Game {self.id_code} , Winner : {self.Winner}, Player 1 : {self.Player_1},Player 2 :{self.Player_2}"
