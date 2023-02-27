from game.models import Game, GameSessionMoves
from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["uuid"]


class GameDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["uuid", "winner", "game_over"]


class GameSessionMovesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSessionMoves
        fields = ["player", "position"]


class GameWithGameMovesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ["uuid", "moves"]

    moves = GameSessionMovesSerializer(many=True, read_only=True, source="gamesessionmoves_set")
