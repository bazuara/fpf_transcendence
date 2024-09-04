from django.shortcuts import render
from .models import Room

def rooms_view(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms.html')
    else:
        return render(request, 'rooms/rooms_full.html')

def rooms_create(request):
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_create.html')
    else:
        return render(request, 'rooms/rooms_create_full.html')
    
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