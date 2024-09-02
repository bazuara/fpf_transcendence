from django.shortcuts import render

def rooms_view(request):
    context = {
        'game_mode' : '1vs1',
        'team1' : 'teamPepe',
        'team2' : 'teamAgus',
        'room_code' : 'Abaunfjkdf'
    }

    if 'HX-Request' in request.headers:
        return render(request, 'rooms/rooms.html', context)
    else:
        return render(request, 'rooms/rooms_full.html', context)