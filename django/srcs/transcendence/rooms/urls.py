from django.urls import path
from .views import (
    rooms_view,
)

urlpatterns = [
    path('rooms/', rooms_view, name='rooms'),
]