from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<str:name>/', social_view, name='profile'),
    path('profile/<str:name>/info', profile_view, name='profile_view'),

    path('profile/<str:name>/change_alias/', change_alias, name='change_alias'),
    path('profile/<str:name>/change_avatar/', change_avatar, name='change_avatar'),
    
    path('profile/<str:name>/friends/', friends_view, name='friends'),
    path('profile/<str:name>/game_history/', game_history_view, name='game_history'),
]