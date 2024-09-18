import json
import threading
import random
import string

from channels.generic.websocket import WebsocketConsumer
from .models import Room, Tournament
from social.models import User as OurUser
from game.models import Game
from asgiref.sync import async_to_sync

lock_dict = {}
global_dict_lock = threading.Lock()
global_tournaments_lock = threading.Lock()

from .consumers_room import global_games_lock

def acquire_lock(key):
    global_dict_lock.acquire()
    try:
        if key not in lock_dict:
            lock_dict[key] = threading.Lock()
        lock = lock_dict[key]
    finally:
        global_dict_lock.release()
    lock.acquire()

def release_lock(key):
    global_dict_lock.acquire()
    try:
        if key in lock_dict:
            lock_dict[key].release()
    finally:
        global_dict_lock.release()

def generate_game_id():
    while True:
        game_id = ''.join(random.choices(string.digits, k=30))
        if not Game.objects.filter(game_id=game_id).exists():
            return game_id


class TournamentConsumer(WebsocketConsumer):

    def connect(self):
        self.accepted = False
        self.tournament_id = self.scope["url_route"]["kwargs"]["tournament_id"]
        self.group_name = "tournament_" + self.tournament_id
        self.user = self.scope["user"]

        if not self.user:
            return
        
        acquire_lock(self.tournament_id)
        try:
            ourUser = OurUser.objects.get(name=self.user.username)
            tournament = Tournament.objects.get(tournament_id=self.tournament_id)

            if not tournament.user1 == ourUser and not tournament.user2 == ourUser and not tournament.user3 == ourUser and not tournament.user4 == ourUser:
                raise Exception
        except:
            self.close()
            return
        finally:
            release_lock(self.tournament_id)

        async_to_sync(self.channel_layer.group_add) (self.group_name, self.channel_name)
        self.accept()
        self.accepted = True
        async_to_sync(self.channel_layer.group_send) (self.group_name, {"type": "state.update"})

    def disconnect(self, close_code):
        if not self.accepted:
            return

        acquire_lock(self.tournament_id)
        try:
            ourUser = OurUser.objects.get(name=self.user.username)
            tournament = Tournament.objects.get(tournament_id=self.tournament_id)
            match ourUser:
                case tournament.user1:
                    tournament.user1_ready = False
                case tournament.user2:
                    tournament.user2_ready = False
                case tournament.user3:
                    tournament.user3_ready = False
                case tournament.user4:
                    tournament.user4_ready = False
                case _:
                    raise Exception
            tournament.save()
            async_to_sync(self.channel_layer.group_send) (self.group_name, {"type": "state.update"})
        except:
            pass
        finally:
            release_lock(self.tournament_id)

        async_to_sync(self.channel_layer.group_discard) (self.group_name, self.channel_name)

    def state_update(self, event):
        acquire_lock(self.tournament_id)

        try:
            tournament = Tournament.objects.get(tournament_id=self.tournament_id)
            ourUser = OurUser.objects.get(name=self.user.username)
            state = {
                "redirect": False,
                "show_button": True,
                "user1": tournament.user1.alias,
                "user2": tournament.user2.alias,
                "user3": tournament.user3.alias,
                "user4": tournament.user4.alias,
            }

            if tournament.game_12 and tournament.game_12.end_time:
                state["winner_12"]  = tournament.game_12.user1.alias if tournament.game_12.score1 > tournament.game_12.score2 else tournament.game_12.user3.alias
                state["score_12_1"] = tournament.game_12.score1
                state["score_12_2"] = tournament.game_12.score2
                if tournament.game_12.user1 == ourUser and tournament.game_12.score1 < tournament.game_12.score2:
                    state["show_button"] = False
                if tournament.game_12.user3 == ourUser and tournament.game_12.score1 > tournament.game_12.score2:
                    state["show_button"] = False
            if tournament.game_34 and tournament.game_34.end_time:
                state["winner_34"]  = tournament.game_34.user1.alias if tournament.game_34.score1 > tournament.game_34.score2 else tournament.game_34.user3.alias
                state["score_34_1"] = tournament.game_34.score1
                state["score_34_2"] = tournament.game_34.score2
                if tournament.game_34.user1 == ourUser and tournament.game_34.score1 < tournament.game_34.score2:
                    state["show_button"] = False
                if tournament.game_34.user3 == ourUser and tournament.game_34.score1 > tournament.game_34.score2:
                    state["show_button"] = False
            if tournament.game_final and tournament.game_final.end_time:
                state["winner_final"]  = tournament.game_final.user1.alias if tournament.game_final.score1 > tournament.game_final.score2 else tournament.game_final.user3.alias
                state["score_final_1"] = tournament.game_final.score1
                state["score_final_2"] = tournament.game_final.score2
                state["show_button"]   = False
            self.send(json.dumps(state))
        finally:
            release_lock(self.tournament_id)

    def assignUserReady(self, ready, ourUser, tournament):
        match ourUser:
            case tournament.user1:
                tournament.user1_ready = ready
            case tournament.user2:
                tournament.user2_ready = ready
            case tournament.user3:
                tournament.user3_ready = ready
            case tournament.user4:
                tournament.user4_ready = ready
            case _:
                raise Exception("user not in tournament")

    def game_12Ready(self, tournament):
        return not tournament.game_12 and (tournament.user1_ready and tournament.user2_ready)

    def game_34Ready(self, tournament):
        return not tournament.game_34 and (tournament.user3_ready and tournament.user4_ready)

    def game_finalReady(self, tournament):
        if not tournament.game_final and tournament.game_12 and tournament.game_12.end_time and tournament.game_34 and tournament.game_34.end_time:
            self.winner_12 = tournament.game_12.user1 if tournament.game_12.score1 > tournament.game_12.score2 else tournament.game_12.user3
            self.winner_34 = tournament.game_34.user1 if tournament.game_34.score1 > tournament.game_34.score2 else tournament.game_34.user3
            self.winner_12_ready = tournament.user1_ready if self.winner_12 == tournament.user1 else tournament.user2_ready
            self.winner_34_ready = tournament.user3_ready if self.winner_34 == tournament.user3 else tournament.user4_ready
            return self.winner_12_ready and self.winner_34_ready

        return False

    def game_ready(self, event):
        self.send(json.dumps({"redirect": True, "player1": event["player1"], "player2": event["player2"], "next_id": event["next_id"], "selfplayer": self.user.username}))

    def receive(self, text_data):
        acquire_lock(self.tournament_id)

        try:
            ourUser = OurUser.objects.get(name=self.user.username)
            tournament = Tournament.objects.get(tournament_id=self.tournament_id)
            match text_data:
                case "ready":
                    self.assignUserReady(True, ourUser, tournament)
                case "cancel":
                    self.assignUserReady(False, ourUser, tournament)
            tournament.save()

            if self.game_12Ready(tournament):
                global_games_lock.acquire()
                try:
                    next_id = generate_game_id()
                    game = Game.objects.create(
                        game_mode='T',
                        game_id=next_id,
                        user1=tournament.user1,
                        user2=None,
                        user3=tournament.user2,
                        user4=None,
                    )
                    tournament.game_12 = game
                finally:
                    global_games_lock.release()
                async_to_sync(self.channel_layer.group_send) (
                    self.group_name, {"type": "game.ready", "player1": tournament.user1.name, "player2": tournament.user2.name, "next_id": next_id}
                )
                tournament.user1_ready = False
                tournament.user2_ready = False
                tournament.save()
            elif self.game_34Ready(tournament):
                global_games_lock.acquire()
                try:
                    next_id = generate_game_id()
                    game = Game.objects.create(
                        game_mode='T',
                        game_id=next_id,
                        user1=tournament.user3,
                        user2=None,
                        user3=tournament.user4,
                        user4=None,
                    )
                    tournament.game_34 = game
                finally:
                    global_games_lock.release()
                async_to_sync(self.channel_layer.group_send) (
                    self.group_name, {"type": "game.ready", "player1": tournament.user3.name, "player2": tournament.user4.name, "next_id": next_id}
                )
                tournament.user3_ready = False
                tournament.user4_ready = False
                tournament.save()
            elif self.game_finalReady(tournament):
                global_games_lock.acquire()
                try:
                    next_id = generate_game_id()
                    game = Game.objects.create(
                        game_mode='T',
                        game_id=next_id,
                        user1=self.winner_12,
                        user2=None,
                        user3=self.winner_34,
                        user4=None,
                    )
                    tournament.game_final = game
                finally:
                    global_games_lock.release()
                async_to_sync(self.channel_layer.group_send) (
                    self.group_name, {"type": "game.ready", "player1": self.winner_12.name, "player2": self.winner_34.name, "next_id": next_id}
                )
                tournament.save()

        finally:
            release_lock(self.tournament_id)
