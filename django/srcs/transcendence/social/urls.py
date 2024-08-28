from django.urls import path
from .views import (
    profile_view,
    friends_view,
)

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('friends/', friends_view, name='friends'),
]