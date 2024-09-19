from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve
from social.models import User as OurUser
from django.contrib.auth import logout

EXEMPT_URLS = [
    # Add any URL paths here that should be exempt from the login requirement
    '/admin/', '/landing/', '/login/', '/auth/callback/', '/check_login_status/', '/error/', '/static_files/admin/'
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name
        if request.user.is_authenticated:
            if request.user.is_superuser:
                if not request.path.startswith('/admin/'):
                    return redirect('/admin/')
            our_user_instance = OurUser.objects.filter(name=request.user.username).first()
            if not our_user_instance and not request.user.is_superuser:
                logout(request)
                return redirect('/landing/')

        # Check if the request is for an exempt URL or the user is authenticated
        if not request.user.is_authenticated and not any(request.path_info.startswith(url) for url in EXEMPT_URLS):
            return redirect(f"{settings.LOGIN_URL}")

        response = self.get_response(request)
        return response
