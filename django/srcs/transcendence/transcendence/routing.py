from django.urls import include, path
from channels.routing import URLRouter

from rooms.routing import websocket_urlpatterns as rooms_websocket_urlpatterns
from social.routing import websocket_urlpatterns as social_websocket_urlpatterns

websocket_urlpatterns = [
    path('', URLRouter(rooms_websocket_urlpatterns)),
    path('', URLRouter(social_websocket_urlpatterns)),
]
