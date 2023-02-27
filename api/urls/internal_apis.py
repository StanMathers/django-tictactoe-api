from django.urls import path

# Local Imports
from api.views.internal_apis import StartGame, GameList, GameDetails, GameMove


urlpatterns = [
    # Information endpoints
    path("games/", GameList.as_view(), name="game_list"),
    path("games/<uuid:uuid>/", GameDetails.as_view(), name="game_details"),
    # Action endpoints
    path("start/", StartGame.as_view(), name="start"),
    path("move/<uuid:uuid>/", GameMove.as_view(), name="move"),
]
