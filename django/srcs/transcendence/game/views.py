from django.shortcuts import render, get_object_or_404
from game.models import Game

# Create your views here.
def game_view(request, gameid):
    get_object_or_404(Game, game_id=gameid)
    if 'HX-Request' in request.headers:
        return render(request, 'game.html')
    else:
        return render(request, 'game_full.html')