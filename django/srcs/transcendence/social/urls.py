from django.urls import path
from .views import *

urlpatterns = [
    path('social/<str:name>/', social_view, name='social'),
    path('social/<str:name>/info', profile_view, name='profile_view'),

    path('social/<str:name>/change_alias/', change_alias, name='change_alias'),
    path('social/<str:name>/change_avatar/', change_avatar, name='change_avatar'),
    
    path('social/<str:name>/friends/', friends_view, name='friends'),
    path('social/<str:name>/game_history/', game_history_view, name='game_history'),

    path('anonymize/<str:name>/', anonymize_view, name='anonymize'),
]