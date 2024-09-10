import os, random, string, requests, time, threading
from django.core.exceptions import ObjectDoesNotExist

from social.models import User as OurUser
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from queue import Queue
from django.urls import reverse

APP_UID = os.getenv("APP_UID")
APP_SECRET = os.getenv("APP_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = 'https://api.intra.42.fr/oauth/token'

# Rate limiting parameters
MAX_REQUESTS_PER_SECOND = 2
REQUEST_INTERVAL = 1 / MAX_REQUESTS_PER_SECOND

# A simple queue to manage incoming requests
request_queue = Queue()

# Lock for synchronized access
lock = threading.Lock()

# Store user information based on session keys
pending_requests = {}

# Worker function to process the queue
def process_queue():
    while True:
        # Get the next request from the queue
        user_info_url, headers, session_key = request_queue.get()

        # Process the request
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        # Store the user info based on session key
        with lock:
            pending_requests[session_key] = user_info

        # Wait to maintain the rate limit
        time.sleep(REQUEST_INTERVAL)

        # Mark the task as done
        request_queue.task_done()

# Start the queue processing thread
thread = threading.Thread(target=process_queue, daemon=True)
thread.start()

def generate_state():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=40))

def login_view(request):
    if request.user.is_authenticated:
        return redirect('welcome')
    
    state = generate_state()
    request.session['oauth_state'] = state
    authorize_url = (
        f"https://api.intra.42.fr/oauth/authorize?client_id={APP_UID}"
        f"&redirect_uri={REDIRECT_URI}&response_type=code&state={state}"
    )
    return redirect(authorize_url)


def auth_callback_view(request):
    state = request.GET.get('state')
    sesion_state = request.session.pop('oauth_state', None)
    if state != sesion_state:
        return HttpResponseBadRequest('Invalid state parameter')

    data = {
        'grant_type'    : 'authorization_code',
        'client_id'     : APP_UID,
        'client_secret' : APP_SECRET,
        'code'          : request.GET.get('code'),
        'redirect_uri'  : REDIRECT_URI,
    }

    response_data = requests.post(TOKEN_URL, data=data).json()
    access_token = response_data.get('access_token')

    # Use the access token to get user info
    user_info_url = 'https://api.intra.42.fr/v2/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    session_key = request.session.session_key
    # Add the request to the queue instead of directly making the request
    request_queue.put((user_info_url, headers, session_key))
    return render(request, 'auth_callback.html')


def handle_user_info_response(request, user_info):
    username = user_info['login']
    user, created = User.objects.get_or_create(username=username)
    login(request, user)
    try:
        existing_user = OurUser.objects.get(name = user_info.get("login"))
        return redirect('welcome')
    except ObjectDoesNotExist:
        OurUser.objects.create(
            name         = user_info.get("login"),
            alias        = user_info.get("login"),
            intra_image  = user_info.get("image").get("link"),
            wins         = 0,
            loses        = 0,
            socket_ctr   = 0,
        )
    return redirect('welcome')

def check_login_status_view(request):
    session_key = request.session.session_key

    with lock:
        if session_key in pending_requests:
            user_info = pending_requests.pop(session_key)
            handle_user_info_response(request, user_info)
            return JsonResponse({'status': 'complete', 'redirect_url': reverse('welcome')})

    return JsonResponse({'status': 'pending'})


def logout_view(request):
    logout(request)
    return redirect('landing')


def landing_view(request):
    if request.user.is_authenticated:
        return 
    return render(request, 'landing.html')
