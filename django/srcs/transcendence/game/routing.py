from django.urls import path

from .consumers import GameConsumer, LocalGameConsumer

websocket_urlpatterns = [
	path("ws/game/local/", LocalGameConsumer.as_asgi()),
	path("ws/game/<str:game_id>/", GameConsumer.as_asgi()),
]
