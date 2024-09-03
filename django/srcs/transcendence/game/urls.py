from django.urls import path
from .views import (
    game_view,
)

urlpatterns = [
    path('game/<str:gameid>/', game_view, name='game_view'),
]