from typing import Literal, Union, List

# Django Imports
from django.db import IntegrityError

# DRF Imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)

# Local Imports
from game.models import Game, GameSessionMoves

# Local Serializers
from api.serializers.game_serializers.serializers import (
    GameSerializer,
    GameDetailsSerializer,
    GameSessionMovesSerializer,
    GameWithGameMovesSerializer,
)


class StartGame(APIView):
    """
    This view starts a new game session and returns the uuid of the game.
    url: /api/start/
    """

    def get(self, request):
        game = Game.objects.create()
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GameList(ListAPIView):
    """
    This method retrives all the started game session uuid
    url: /api/games/
    """

    serializer_class = GameDetailsSerializer
    queryset = Game.objects.all()


class GameDetails(RetrieveAPIView):
    """
    This method retrives a detail for a single game session with uuid
    url: /api/games/<uuid:uuid>/
    """

    serializer_class = GameDetailsSerializer
    queryset = Game.objects.all()
    lookup_field = "uuid"


class GameCheck(APIView):
    """
    This method checks if the game is in progress or finished
    url: /api/check/<uuid:uuid>/
    """

    def get(self, request, uuid):
        queryset = Game.objects.filter(uuid=uuid).first()
        if queryset.game_over:
            return Response({"game": "finished", "winner": queryset.winner})
        return Response({"game": "in progress"})


class GameHistory(ListAPIView):
    """
    This method retrives all the game sessions with their moves
    url: /api/history/
    """

    serializer_class = GameWithGameMovesSerializer
    queryset = Game.objects.prefetch_related("gamesessionmoves_set").all()


class GameMove(APIView):
    """
    This method is responsible for making a move in the game session,
    checking winner and raising an error if the game is finished when putting a move
    url: /api/move/<uuid:uuid>/
    """

    winner_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    # Serializer Methods
    def get_queryset_game(self):
        return Game.objects.filter(uuid=self.kwargs.get("uuid"))

    def get_queryset(self):
        return GameSessionMoves.objects.filter(game__uuid=self.kwargs.get("uuid"))

    def get_serializer(self, **kwargs):
        return GameSessionMovesSerializer(**kwargs)

    # Custom Methods
    def get_positions_for_player(self, player: Literal["X", "O"]) -> List[int]:
        # This method returns a list of positions for a given player. [1, 2, 3...]
        data = self.get_queryset().filter(player=player)
        return [move.position for move in data]

    def just_won(self, combinations: List[int]) -> bool:
        # This method checks if a given list of positions is a winning combination
        for i in self.winner_combinations:
            if i == combinations:
                return True
        return False

    def perform_winner_check(self, player: Literal["X", "O"]) -> Union[bool, None]:
        # This method checks if a player has won the game and updates the game object
        positions = self.get_positions_for_player(player)
        if len(positions) >= 3:
            for i in self.winner_combinations:
                if self.just_won([x for x in i if x in positions]):
                    game = self.get_queryset_game().first()
                    game.winner = player
                    game.game_over = True
                    game.save()

        return False

    def perform_game_over_check(self):
        # This method checks if the game is over and raises an error if it is
        if self.get_queryset_game().first().game_over:
            raise ValidationError("Game is already over")

    # Methods
    def get(self, request, uuid):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, uuid):
        self.perform_game_over_check()

        game = self.get_queryset_game().first()
        player = request.data.get("player")

        try:
            serializer = GameSessionMovesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(game=game)
        except IntegrityError:
            raise ValidationError({"result": "error", "error_code": "Invalid Position"})

        self.perform_winner_check(player)

        return Response({"message": "success"}, status=status.HTTP_201_CREATED)
