from django.db import models
import random
import string
from django.db import models
from django.contrib.auth.models import User


def generate_random_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f'{code[:5]}-{code[5:]}'


class Game(models.Model):
    id_code = models.CharField(max_length=11, default=generate_random_code, unique=True)
    private = models.BooleanField(default=False)
    isfinished = models.BooleanField(default=False)
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()
    alignment = models.IntegerField()
    player_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_1_games', db_column='player_1')
    player_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_2_games', db_column='player_2',
                                 null=True, blank=True, default="null")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='winner_games',
                               db_column='winner')

    def __str__(self):
        return f"Game {self.id_code}"
