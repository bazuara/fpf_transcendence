from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User as OurUser
import asyncio

lock_dict = {}
global_dict_lock = asyncio.Lock()

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

class OnlineConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if self.user is not None:
            try:
                await acquire_lock(self.user.username)
                user = await OurUser.objects.aget(name=self.user.username)
                user.socket_ctr += 1
                await user.asave()
                await release_lock(self.user.username)
                await self.accept()
            except OurUser.DoesNotExist:
                pass

    async def disconnect(self, close_code):
        self.user = self.scope["user"]

        if self.user is not None:
            try:
                await acquire_lock(self.user.username)
                user = await OurUser.objects.aget(name=self.user.username)
                user.socket_ctr -= 1
                await user.asave()
                await release_lock(self.user.username)
            except OurUser.DoesNotExist:
                pass

    async def receive(self, text_data):
        pass