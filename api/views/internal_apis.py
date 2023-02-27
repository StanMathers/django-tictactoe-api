from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

# Local Imports
from game.models import Game, GameSessionMoves

# Local Serializers
from api.serializers.game_serializers.serializers import (
    GameSerializer,
    GameDetailsSerializer,
    GameSessionMovesSerializer,
)


class StartGame(APIView):
    def get(self, request):
        game = Game.objects.create()
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GameList(ListAPIView):
    serializer_class = GameDetailsSerializer
    queryset = Game.objects.all()


class GameDetails(RetrieveAPIView):
    serializer_class = GameDetailsSerializer
    queryset = Game.objects.all()
    lookup_field = "uuid"
