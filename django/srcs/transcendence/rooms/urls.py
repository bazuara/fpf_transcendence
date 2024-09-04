from django.urls import path
from .views import (
    rooms_view,
    rooms_create,
    rooms_join,
    rooms_join_public,
    rooms_join_private,
    rooms_detail,
)

urlpatterns = [
    path('rooms/', rooms_view, name='rooms'),
    path('rooms/create', rooms_create, name='rooms_create'),
    path('rooms/join', rooms_join, name='rooms_join'),
    path('rooms/join/public', rooms_join_public, name='rooms_join_public'),
    path('rooms/join/private', rooms_join_private, name='rooms_join_private'),
    path('rooms/<str:room_id>', rooms_detail, name='rooms_detail'),
]