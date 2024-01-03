from django.db import models
from django.contrib.auth.models import User

# ANCIEN MODEL USER INUTILE
'''class User(models.Model):
    PlayerName = models.CharField(max_length=50)
    PlayerFirstName = models.CharField(max_length=50)
    PlayerLastName = models.CharField(max_length=50)
    PlayerPassword = models.CharField(max_length=500)
    PlayerBirthDate = models.DateField()
    PlayerScore = models.PositiveIntegerField()
    PlayerEmail = models.EmailField()'''


class CommunityMessage(models.Model):
    date = models.DateField(auto_now_add=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    has_been_treated=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.date}"
