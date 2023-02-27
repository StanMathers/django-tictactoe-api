from django.urls import path

# Local Imports
from api.views.internal_apis import StartGame, GameList, GameDetails


urlpatterns = [
    path("games/", GameList.as_view(), name="game_list"),
    path("games/<uuid:uuid>/", GameDetails.as_view(), name="game_details"),
    path("start/", StartGame.as_view(), name="start"),
]
