from django.urls import path
from .views import (
    welcome_view,
    about_view,
    how_to_play_view,
)

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('about/', about_view, name='about'),
    path('how_to_play/', how_to_play_view, name='how_to_play'),
]
