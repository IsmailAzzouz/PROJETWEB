# Generated by Django 4.2.7 on 2023-11-19 17:15

import Game.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_code', models.CharField(default=Game.models.generate_random_code, max_length=11, unique=True)),
                ('private', models.BooleanField(default=False)),
                ('grid_x', models.IntegerField()),
                ('grid_y', models.IntegerField()),
                ('alignment', models.IntegerField()),
                ('player_1', models.ForeignKey(default='Player_1', on_delete=django.db.models.deletion.CASCADE, related_name='player_1_games', to=settings.AUTH_USER_MODEL)),
                ('player_2', models.ForeignKey(default='Player_2', on_delete=django.db.models.deletion.CASCADE, related_name='player_2_games', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner_games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
