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
global_games_lock = threading.Lock()
global_tournaments_lock = threading.Lock()

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

def generate_tournament_id():
    while True:
        tournament_id = ''.join(random.choices(string.digits, k=6))
        if not Tournament.objects.filter(tournament_id=tournament_id).exists():
            return tournament_id


class RoomConsumer(WebsocketConsumer):

    def connect(self):
        self.accepted = False
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.group_name = "room_" + self.room_id
        self.user = self.scope["user"]

        if not self.user:
            return
        
        acquire_lock(self.room_id)
        try:
            ourUser = OurUser.objects.get(name=self.user.username)
            room = Room.objects.get(room_id=self.room_id)

            if room.user1 == ourUser or room.user2 == ourUser or room.user3 == ourUser or room.user4 == ourUser:
                raise Exception
            elif room.user1 is None:
                room.user1 = ourUser
            elif room.game_mode == "1":
                if room.user3 is None:
                    room.user3 = ourUser
                else:
                    raise Exception
            else:
                if room.user2 is None:
                    room.user2 = ourUser
                elif room.user3 is None:
                    room.user3 = ourUser
                elif room.user4 is None:
                    room.user4 = ourUser
                else:
                    raise Exception
            room.save()
        except:
            return
        finally:
            release_lock(self.room_id)

        async_to_sync(self.channel_layer.group_add) (self.group_name, self.channel_name)
        self.accept()
        self.accepted = True
        async_to_sync(self.channel_layer.group_send) (self.group_name, {"type": "state.update"})

    def disconnect(self, close_code):
        if not self.accepted:
            return

        acquire_lock(self.room_id)
        try:
            ourUser = OurUser.objects.get(name=self.user.username)
            room = Room.objects.get(room_id=self.room_id)
            match ourUser:
                case room.user1:
                    room.user1 = None
                    room.user1_ready = False
                case room.user2:
                    room.user2 = None
                    room.user2_ready = False
                case room.user3:
                    room.user3 = None
                    room.user3_ready = False
                case room.user4:
                    room.user4 = None
                    room.user4_ready = False
                case _:
                    raise Exception
            room.save()
            async_to_sync(self.channel_layer.group_send) (self.group_name, {"type": "state.update"})
        except:
            pass
        finally:
            release_lock(self.room_id)

        async_to_sync(self.channel_layer.group_discard) (self.group_name, self.channel_name)

    def state_update(self, event):
        acquire_lock(self.room_id)

        try:
            room = Room.objects.get(room_id=self.room_id)
            state = {}

            if room.user1 is not None:
                state["user1"] = room.user1.alias
            if room.user2 is not None:
                state["user2"] = room.user2.alias
            if room.user3 is not None:
                state["user3"] = room.user3.alias
            if room.user4 is not None:
                state["user4"] = room.user4.alias
            self.send(json.dumps(state))
        finally:
            release_lock(self.room_id)

    def ready(self, event):
        self.send(json.dumps({"redirect": True, "game_mode": event["game_mode"], "next_id": event["next_id"]}))

    def assignUserReady(self, ready, ourUser, room):
        match ourUser:
            case room.user1:
                room.user1_ready = ready
            case room.user2:
                room.user2_ready = ready
            case room.user3:
                room.user3_ready = ready
            case room.user4:
                room.user4_ready = ready
            case _:
                raise Exception("user not in room")

    def allUsersReady(self, room):
        if (room.game_mode == "1"):
            return room.user1_ready and room.user3_ready
        return room.user1_ready and room.user2_ready and room.user3_ready and room.user4_ready

    def receive(self, text_data):
        acquire_lock(self.room_id)

        try:
            ourUser = OurUser.objects.get(name=self.user.username)
            room = Room.objects.get(room_id=self.room_id)
            match text_data:
                case "ready":
                    self.assignUserReady(True, ourUser, room)
                case "cancel":
                    self.assignUserReady(False, ourUser, room)
            room.save()

            if self.allUsersReady(room):
                if room.game_mode == "T":
                    global_tournaments_lock.acquire()
                    try:
                        next_id = generate_tournament_id()
                        Tournament.objects.create(
                            tournament_id=next_id,
                            user1=room.user1,
                            user2=room.user2,
                            user3=room.user3,
                            user4=room.user4,
                        )
                    finally:
                        global_tournaments_lock.release()
                else:
                    global_games_lock.acquire()
                    try:
                        next_id = generate_game_id()
                        Game.objects.create(
                            game_id=next_id,
                            user1=room.user1,
                            user2=room.user2,
                            user3=room.user3,
                            user4=room.user4,
                        )
                    finally:
                        global_games_lock.release()
                del lock_dict[self.room_id]
                async_to_sync(self.channel_layer.group_send) (
                    self.group_name, {"type": "ready", "game_mode": room.game_mode, "next_id": next_id}
                )
                Room.objects.get(room_id=self.room_id).delete()
        finally:
            release_lock(self.room_id)
