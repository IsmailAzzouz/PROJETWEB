# Generated by Django 4.2.7 on 2024-01-03 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HelbMorpion', '0006_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='communitymessage',
            name='hasbeentreated',
            field=models.BooleanField(default=False),
        ),
    ]
