from django.shortcuts import render, redirect, get_object_or_404
from rooms.models import Room
from django.http import HttpResponseBadRequest
import random
import string
from .forms import RoomForm

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

def rooms_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            game_mode = form.cleaned_data['game_mode']
            is_public = form.cleaned_data['is_public'] == True

            room_id = generate_room_id()

            new_room = Room.objects.create(
                game_mode=game_mode,
                room_id=room_id,
                is_public=is_public
            )
            context = {
                'room' : new_room,
            }
            if 'HX-Request' in request.headers:
                return render(request, 'rooms/room_created.html', context)
            else:
                return render(request, 'rooms/room_created_full.html', context)
    
    else:
        form = RoomForm()

    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_create.html', {'form': form})
    else:
        return render(request, 'rooms/rooms_create_full.html', {'form': form})

def rooms_join(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join.html')
    else:
        return render(request, 'rooms/rooms_join_full.html')
    
def rooms_join_public(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join_public.html')
    else:
        return render(request, 'rooms/rooms_join_public_full.html')
    
def rooms_join_private(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join_private.html')
    else:
        return render(request, 'rooms/rooms_join_private_full.html')
