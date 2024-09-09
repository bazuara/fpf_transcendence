from django.urls import path

from .consumers import RoomConsumer

websocket_urlpatterns = [
	path("ws/rooms/<str:room_id>/", RoomConsumer.as_asgi()),
]
