import asyncio
import time
import random
import math

from channels.generic.websocket import AsyncWebsocketConsumer
from .game import GameHandler
from .models import Game
from social.models import User as OurUser
from asgiref.sync import sync_to_async

lock_dict = {}
global_dict_lock = asyncio.Lock()
games_dict = {}

async def acquire_lock(key):
    await global_dict_lock.acquire()
    try:
        if key not in lock_dict:
            lock_dict[key] = asyncio.Lock()
        lock = lock_dict[key]
    finally:
        global_dict_lock.release()
    await lock.acquire()

async def release_lock(key):
    await global_dict_lock.acquire()
    try:
        if key in lock_dict:
            lock_dict[key].release()
    finally:
        global_dict_lock.release()

class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.group_name = "game_" + self.game_id
        self.user = self.scope["user"]

        if not self.user:
            self.close()
            return

        await acquire_lock(self.game_id)
        try:
            ourUser = await OurUser.objects.aget(name=self.user.username)
            game = await Game.objects.aget(game_id=self.game_id)
            
            await self.set_user_connected(ourUser, game)

            if game.user1_connected and game.user3_connected and not game.game_started:
                game.game_started = True
                games_dict[self.game_id] = GameHandler(self.game_id, game.game_mode == "2")

            await game.asave()
        except:
            self.close()
            return
        finally:
            await release_lock(self.game_id)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def receive(self, text_data):
        try:
            games_dict[self.game_id].setPaddleMove(self.player_n, text_data)
        except:
            pass

    async def state_update(self, event):
        await self.send(event["state"])

    async def end_game(self, event):
        await self.send(event["message"])

    async def game_ready(self, game):
        if game.game_mode == "1" or game.game_mode == "T":
            return game.user1_connected and game.user3_connected and not game.game_started
        return game.user1_connected and game.user2_connected and game.user3_connected and game.user4_connected and not game.game_started

    @sync_to_async
    def set_user_connected(self, ourUser, game):
        match ourUser:
            case game.user1:
                self.player_n = 0
                game.user1_connected = True
            case game.user2:
                self.player_n = 2
                game.user2_connected = True
            case game.user3:
                self.player_n = 1
                game.user3_connected = True
            case game.user4:
                self.player_n = 3
                game.user4_connected = True
            case _:
                raise Exception
