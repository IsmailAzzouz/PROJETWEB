# Generated by Django 4.2.7 on 2023-12-27 17:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0002_game_hassurrend'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='hasSurrend',
            new_name='has_surrendered',
        ),
    ]