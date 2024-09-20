from datetime import datetime
from django.utils import timezone
from .consumers_room import lock_dict as room_lock_dict
from .consumers_tournament import lock_dict as tournament_lock_dict
from tournaments.views import save_tournament
from rooms.models import Room, Tournament

def delete_empty_rooms():
    print("Deleting empty rooms...")
    time_now = timezone.now()
    empty_rooms = Room.objects.filter(user1=None, user2=None, user3=None, user4=None)
    for room in empty_rooms:
        if (time_now - room.updated_at).total_seconds() > 30:
            if room.room_id in room_lock_dict:
                del room_lock_dict[room.room_id]
            room.delete()

def delete_write_finished_tournaments():
    print("Writting tournaments in blockchain...")
    print("Deleting empty tournaments...")
    done_tournaments = Tournament.objects.filter(game_final__end_time__isnull=False)
    for tournament in done_tournaments:
        data = {
            "player_id_1": str(tournament.user1.id),
            "player_id_2": str(tournament.user2.id),
            "player_id_3": str(tournament.user3.id),
            "player_id_4": str(tournament.user4.id),
            "score_match_1_2": str(tournament.game_12.score1) + "-" + str(tournament.game_12.score2),
            "score_match_3_4": str(tournament.game_34.score1) + "-" + str(tournament.game_34.score2),
            "score_match_final": str(tournament.game_final.score1) + "-" + str(tournament.game_final.score2),
        }
        if tournament.tournament_id in tournament_lock_dict:
            del tournament_lock_dict[tournament.tournament_id]
        save_tournament(data)
        tournament.delete()
        tournament.game_12.delete()
        tournament.game_34.delete()
        tournament.game_final.delete()