from django.urls import path

from .consumers_room import RoomConsumer
from .consumers_tournament import TournamentConsumer

websocket_urlpatterns = [
    path("ws/rooms/<str:room_id>/", RoomConsumer.as_asgi()),
    path("ws/rooms/tournament/<str:tournament_id>/", TournamentConsumer.as_asgi()),
]
