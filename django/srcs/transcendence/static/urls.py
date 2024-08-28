from django.urls import path
from .views import (
    welcome_view,
    about_view,
)

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('about/', about_view, name='about'),
]
