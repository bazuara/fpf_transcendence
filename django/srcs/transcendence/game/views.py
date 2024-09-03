from django.shortcuts import render, get_object_or_404
from game.models import Game

# Create your views here.
def game_view(request, gameid):
    game = get_object_or_404(Game, game_id=gameid)
    context = {
        'game': game
	}
    if 'HX-Request' in request.headers:
        return render(request, 'game.html', context)
    else:
        return render(request, 'game_full.html', context)