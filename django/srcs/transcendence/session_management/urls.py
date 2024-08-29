from django.urls import path
from .views import (
    login_view,
    auth_callback_view,
    check_login_status_view,

    logout_view,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('auth/callback/', auth_callback_view, name='auth_callback'),
    path('check_login_status/', check_login_status_view, name='check_login_status'),

    path('logout/', logout_view, name='logout'),
]