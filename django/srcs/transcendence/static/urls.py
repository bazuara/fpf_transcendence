from django.urls import path
from .views import (
    index_view,
    about_view,
)

urlpatterns = [
    path('', index_view, name='index'),
    path('about/', about_view, name='about'),
]
