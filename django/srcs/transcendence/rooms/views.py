from django.shortcuts import render, get_object_or_404
from rooms.models import Room
import random
import string
from .forms import RoomForm
from django.http import HttpResponseForbidden

room_ids = {}

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
    global room_ids

    if request.method == 'POST':
        try:
            room_id = room_ids[request.user.username]
        except:
            return HttpResponseForbidden()

        form = RoomForm(request.POST)

        if (Room.objects.filter(room_id=room_id).exists()):
            return HttpResponseForbidden()
    
        if form.is_valid():
            game_mode = form.cleaned_data['game_mode']
            is_public = form.cleaned_data['is_public']

            del room_ids[request.user.username]
            
            room = Room.objects.create(
                game_mode=game_mode,
                room_id=room_id,
                is_public=is_public,
            )
            context = {
                'room' : room,
            }
            if 'HX-Request' in request.headers:
                return render(request, 'rooms/rooms_detail.html', context)
            else:
                return render(request, 'rooms/rooms_detail_full.html', context)
        else:
            return HttpResponseForbidden()

    form = RoomForm()
    room_id = generate_room_id()
    room_ids[request.user.username] = room_id


    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_create.html', {'form': form, 'room_id': room_id})
    else:
        return render(request, 'rooms/rooms_create_full.html', {'form': form, 'room_id': room_id})

def rooms_detail(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    context = {
        'room' : room,
    }

    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_detail.html', context)
    else:
        return render(request, 'rooms/rooms_detail_full.html', context)

def rooms_join(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join.html')
    else:
        return render(request, 'rooms/rooms_join_full.html')
    
def rooms_join_public(request):
    context = {}
    context['rooms'] = Room.objects.filter(is_public=True).all()

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
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_join_private.html')
    else:
        return render(request, 'rooms/rooms_join_private_full.html')
