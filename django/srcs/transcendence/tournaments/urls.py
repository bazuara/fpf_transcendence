from django.urls import path
from .views import *

urlpatterns = [
    path('tournaments/', tournament_view, name='tournaments'),
]