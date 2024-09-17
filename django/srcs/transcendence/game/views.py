from django.http import Http404
from django.shortcuts import render, get_object_or_404
from game.models import Game

# Create your views here.
def game_view(request, game_id):
    game_instance = get_object_or_404(Game, game_id=game_id)
    if game_instance.end_time:
        raise Http404("No Game matches the given query.")
    if 'HX-Request' in request.headers:
        return render(request, 'game.html')
    else:
        return render(request, 'game_full.html')