from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<str:name>/', profile_view, name='profile'),
    path('profile/<str:name>/change_alias/', change_alias, name='change_alias'),
    path('profile/<str:name>/change_avatar/', change_avatar, name='change_avatar'),
    
    path('friends/', friends_view, name='friends'),
]