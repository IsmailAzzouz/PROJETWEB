from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    user_score = models.PositiveIntegerField(default=0)
    user_rank = models.PositiveIntegerField(default=0)
    user_gameplayed = models.PositiveIntegerField(default=0)
    user_game_won = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 512 or img.width > 512:
            new_width = min(img.width, 512)
            new_height = min(img.height, 512)

            left = (img.width - new_width) / 2
            top = (img.height - new_height) / 2
            right = (img.width + new_width) / 2
            bottom = (img.height + new_height) / 2

            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)
