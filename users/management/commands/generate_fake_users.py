# your_app/management/commands/generate_fake_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile  # Import your Profile model
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Generate fake users for demonstration purposes'

    def handle(self, *args, **options):
        fake = Faker()

        for _ in range(28):  # Change 10 to the desired number of fake users
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',  # Set a default password for all users
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

            # Access the profile of the user and update the fields
            profile = user.profile
            profile.user_score = random.randint(1, 1000)
            profile.user_gameplayed = random.randint(1, 1000)
            profile.user_game_won = random.randint(1, 1000)
            profile.user_rank = random.randint(1, 1000)

            # Save the profile changes
            profile.save()

        self.stdout.write(self.style.SUCCESS('Fake users and profiles created successfully'))
