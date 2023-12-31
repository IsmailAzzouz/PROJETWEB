# models.py

from django.db import models
from django.contrib.auth.models import User
import random
import string

def generate_random_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return f'{code[:5]}-{code[5:]}'

class Game(models.Model):
    id_code = models.CharField(max_length=11, default=generate_random_code, unique=True)
    private = models.BooleanField(default=False)
    isfinished = models.BooleanField(default=False)
    has_surrendered = models.BooleanField(default=False)
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()
    alignment = models.IntegerField()
    player_1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_1_games', db_column='player_1')
    player_2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_2_games', db_column='player_2',
                                 null=True, blank=True, default="null")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='winner_games',
                               db_column='winner')
    nextplayer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='nextplayer_games',
                               db_column='nextplayer')
    game_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Game {self.id_code}"

    def save(self, *args, **kwargs):
        # Call the save method of the parent class (Model) to ensure the game is saved
        super(Game, self).save(*args, **kwargs)

        # Check if the game does not have an associated grid
        if not hasattr(self, 'grid'):
            # Create a grid and associated cells for the game
            new_grid = Grid.objects.create(game=self, grid_x=self.grid_x, grid_y=self.grid_y)
            new_grid.create_cells()

class Grid(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name='grid')
    grid_x = models.IntegerField()
    grid_y = models.IntegerField()

    def create_cells(self):
        # Create cells for the grid based on grid_x and grid_y
        for x in range(self.grid_x):
            for y in range(self.grid_y):
                Cell.objects.create(grid=self, x_position=x, y_position=y)

    def __str__(self):
        return f"Grid for Game {self.game.id_code}"

class Cell(models.Model):
    grid = models.ForeignKey(Grid, on_delete=models.CASCADE, related_name='cells')
    x_position = models.IntegerField()
    y_position = models.IntegerField()
    value = models.CharField(max_length=1, default='', blank=True)

    def __str__(self):
        return f"Cell ({self.x_position}, {self.y_position}) in Grid for Game {self.grid.game.id_code}"
