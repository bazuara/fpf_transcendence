from django.shortcuts import render, get_object_or_404
from game.models import Game

def game_view(request, game_id):
    get_object_or_404(Game, game_id=game_id)
    if 'HX-Request' in request.headers:
        return render(request, 'game.html')
    else:
        return render(request, 'game_full.html')

def game_local_view(request):
    if 'HX-Request' in request.headers:
        return render(request, 'game_local.html')
    else:
        return render(request, 'game_local_full.html')
