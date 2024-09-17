from django.shortcuts import render, get_object_or_404
from rooms.models import Room, Tournament
import random, threading
import string
from .forms import RoomForm, JoinPrivateForm
from django.http import HttpResponseForbidden
from datetime import datetime
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from .consumers_room import lock_dict

rooms_lock = threading.Lock()
# This error msg will be used when joining both private/public rooms
ROOM_FULL_ERR_MSG = 'Room is full! :('

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_empty_rooms, 'interval', minutes=5)
    scheduler.start()

def delete_empty_rooms():
    print("Deleting empty rooms...")
    time_now = timezone.now()
    empty_rooms = Room.objects.filter(user1=None, user2=None, user3=None, user4=None)
    for room in empty_rooms:
        if (time_now - room.updated_at).total_seconds() > 30:
            if room.room_id in lock_dict:
                del lock_dict[room.room_id]
            room.delete()

def rooms_view(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms.html')
    else:
        return render(request, 'rooms/rooms_full.html')

def generate_room_id():
    while True:
        room_id = ''.join(random.choices(string.digits, k=6))
        if not Room.objects.filter(room_id=room_id).exists():
            return room_id

def roomIsFull(room):
    if room.game_mode == '1':
        return room.user1 is not None and room.user3 is not None
    return room.user1 is not None and room.user2 is not None and room.user3 is not None and room.user4 is not None

def rooms_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            game_mode = form.cleaned_data['game_mode']
            is_public = form.cleaned_data['is_public']

            rooms_lock.acquire()
            room_id = generate_room_id()
            room = Room.objects.create(
                game_mode=game_mode,
                room_id=room_id,
                is_public=is_public,
                user1=None,
                user2=None,
                user3=None,
                user4=None,
            )
            rooms_lock.release()

            context = {
                'room' : room,
                'game_mode_human' : room.get_game_mode_display(),
            }
            if 'HX-Request' in request.headers:
                response = render(request, 'rooms/rooms_detail.html', context)
                
            else:
                response = render(request, 'rooms/rooms_detail_full.html', context)
            response['HX-Push-Url'] = f"/rooms/{room_id}"
            return response
    else:
        form = RoomForm()

    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_create.html', {'form': form})
    else:
        return render(request, 'rooms/rooms_create_full.html', {'form': form})

def rooms_detail(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    if roomIsFull(room) is False:
        context = {
            'room' : room,
            'game_mode_human' : room.get_game_mode_display(),
        }
        if 'HX-Request' in request.headers:
            return render(request, 'rooms/rooms_detail.html', context)
        else:
            return render(request, 'rooms/rooms_detail_full.html', context)
    else:
        context = {}
        context['rooms'] = Room.objects.filter(is_public=True).all()
        context['error'] = ROOM_FULL_ERR_MSG

        for room in context['rooms']:
            ctr = 0
            for user in [room.user1, room.user2, room.user3, room.user4]:
                if user:
                    ctr += 1
            room.user_count = ctr
            room.users = [room.user1, room.user2, room.user3, room.user4]

        if 'HX-Request' in request.headers:
            response = render(request, 'rooms/rooms_join_public.html', context)
            response['HX-Push-Url'] = '/rooms/join/public'
            return response
        else:
            return HttpResponseForbidden(ROOM_FULL_ERR_MSG)

def rooms_join(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join.html')
    else:
        return render(request, 'rooms/rooms_join_full.html')
    
def rooms_join_public(request):
    context = {}
    context['rooms'] = Room.objects.filter(is_public=True).all()
    context['error'] = None

    for room in context['rooms']:
        ctr = 0
        for user in [room.user1, room.user2, room.user3, room.user4]:
            if user:
                ctr += 1
        room.user_count = ctr
        room.users = [room.user1, room.user2, room.user3, room.user4]

    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join_public.html', context)
    else:
        return render(request, 'rooms/rooms_join_public_full.html', context)
    
def rooms_join_private(request):
    if request.method == 'POST':
        form = JoinPrivateForm(request.POST)
    
        if form.is_valid():
            room_id = form.cleaned_data['room_id']
            try:
                room = Room.objects.get(room_id=room_id)
                context = {
                    'room' : room,
                    'game_mode_human' : room.get_game_mode_display(),
                }
                if roomIsFull(room) is False:
                    if 'HX-Request' in request.headers:
                        response = render(request, 'rooms/rooms_detail.html', context)
                    else:
                        response = render(request, 'rooms/rooms_detail_full.html', context)
                    response['HX-Push-Url'] = f"/rooms/{room_id}"
                    return response
                else:
                    form.add_error('room_id', ROOM_FULL_ERR_MSG)
            except Room.DoesNotExist:
                form.add_error('room_id', 'Invalid room id')
    else:
        form = JoinPrivateForm()

    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join_private.html', {'form': form})
    else:
        return render(request, 'rooms/rooms_join_private_full.html', {'form': form})

def tournament_room(request, tournament_id):
    tournament = get_object_or_404(Tournament, tournament_id=tournament_id)

    context = {
        'tournament': tournament,
    }

    if 'HX-Request' in request.headers:
        return render(request, 'tournament_room/tournament_room.html', context)
    else:
        return render(request, 'tournament_room/tournament_room_full.html', context)
