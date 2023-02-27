import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Game(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    winner = models.CharField(
        max_length=1, choices=[("X", "X"), ("O", "O")], null=True, blank=True
    )
    game_over = models.BooleanField(default=False)

    def __str__(self):
        return str(self.uuid)


class GameSessionMoves(models.Model):
    """
    0 1 2
    3 4 5
    6 7 8
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.CharField(max_length=1, choices=[("X", "X"), ("O", "O")])
    position = models.IntegerField(
        validators=[MaxValueValidator(8), MinValueValidator(0)]
    )

    class Meta:
        unique_together = ["game", "position"]

    def __str__(self):
        return f"{self.game}: {self.player} - {self.position}"
