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
    """Genera un identificador único para la sala (ejemplo básico)."""
    return ''.join(random.choices(string.digits, k=6))

def rooms_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            game_mode = form.cleaned_data['game_mode']
            is_public = form.cleaned_data['is_public'] == 'Public'
            
            # Generar un room_id único
            room_id = generate_room_id()
            
            # Crear una nueva sala
            new_room = Room.objects.create(
                game_mode=game_mode,
                room_id=room_id,
                is_public=is_public
            )
            
            # Redirigir a la nueva sala creada
            return redirect('rooms_detail', new_room.room_id)
        else:
            return HttpResponseBadRequest("Datos del formulario inválidos.")
    
    else:
        form = RoomForm()
    
    # Renderizar el formulario de creación de sala
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

def rooms_detail(request, room_id):
    room = get_object_or_404(Room, room_id=room_id)
    context = {
        'room_id' : room.room_id,
        'game_mode' : room.game_mode,
        'is_public' : room.is_public,
    }
    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms_detail.html', context)
    else:
        return render(request, 'rooms/rooms_detail_full.html', context)