from django.db import models

# Create your models here.
from django.db import models
import random
import string

def generate_random_code():
    """Generate a random code consisting of 5 letters and 5 numbers."""
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f'{code[:5]}-{code[5:]}'

from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    id_code = models.CharField(max_length=11, default=generate_random_code, unique=True)
    private = models.BooleanField(default=False)
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()
    alignment = models.IntegerField()
    player_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_1_games')
    player_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_2_games')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='winner_games')

    def __str__(self):
        return f"Game {self.id_code}"
