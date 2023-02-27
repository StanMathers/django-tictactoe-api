# Generated by Django 4.1.5 on 2023-02-27 07:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="gamesessionmoves",
            name="game_over",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="gamesessionmoves",
            name="winner",
            field=models.CharField(
                blank=True, choices=[("X", "X"), ("O", "O")], max_length=1, null=True
            ),
        ),
    ]