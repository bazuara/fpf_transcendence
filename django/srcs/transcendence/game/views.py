from django.http import Http404
from django.shortcuts import render, get_object_or_404
from game.models import Game
from apscheduler.schedulers.background import BackgroundScheduler
from .consumers import lock_dict, games_dict

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_finished_games_dicts, 'interval', minutes=5)
    scheduler.start()

def delete_finished_games_dicts():
    print("Clearing finished games...")
    finished_games = Game.objects.filter(end_time__isnull=False, cleared=False)
    for game in finished_games:
        if game.game_id in lock_dict:
            del lock_dict[game.game_id]
        if game.game_id in games_dict:
            del games_dict[game.game_id]
        game.cleared = True
        game.save()

def game_view(request, game_id):
    game_instance = get_object_or_404(Game, game_id=game_id)
    if game_instance.end_time:
        raise Http404("No Game matches the given query.")
    if 'HX-Request' in request.headers:
        return render(request, 'game.html')
    else:
        return render(request, 'game_full.html')

def game_local_view(request):
    if 'HX-Request' in request.headers:
        return render(request, 'game_local.html')
    else:
        return render(request, 'game_local_full.html')
