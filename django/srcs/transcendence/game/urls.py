from django.urls import path
from .views import (
    game_view,
)

urlpatterns = [
    path('game/<str:game_id>/', game_view, name='game_view'),
]