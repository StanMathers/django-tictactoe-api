# Generated by Django 4.1.5 on 2023-02-27 07:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GameSessionMoves",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "player",
                    models.CharField(choices=[("X", "X"), ("O", "O")], max_length=1),
                ),
                (
                    "move",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MaxValueValidator(8),
                            django.core.validators.MinValueValidator(0),
                        ]
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="game.game"
                    ),
                ),
            ],
        ),
    ]