from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

EXEMPT_URLS = [
    # Add any URL paths here that should be exempt from the login requirement
    '/admin/', '/landing/', '/login/', '/auth/callback/', '/check_login_status/', '/error/'
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_name = resolve(request.path_info).url_name
        # Check if the request is for an exempt URL or the user is authenticated
        if not request.user.is_authenticated and not any(request.path_info.startswith(url) for url in EXEMPT_URLS):
            return redirect(f"{settings.LOGIN_URL}")
        
        response = self.get_response(request)
        return response
