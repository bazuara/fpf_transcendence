from django.urls import path
from .views import (
    game_view,
    game_local_view,
)

urlpatterns = [
    path('game/local/', game_local_view, name='game_local_view'),
    path('game/<str:game_id>/', game_view, name='game_view'),
]