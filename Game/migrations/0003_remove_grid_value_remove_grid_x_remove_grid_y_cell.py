# Generated by Django 4.2.7 on 2023-11-22 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Game', '0002_grid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grid',
            name='value',
        ),
        migrations.RemoveField(
            model_name='grid',
            name='x',
        ),
        migrations.RemoveField(
            model_name='grid',
            name='y',
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('value', models.CharField(default='', max_length=1)),
                ('grid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Game.grid')),
            ],
        ),
    ]
