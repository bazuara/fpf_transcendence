from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User as OurUser

class OnlineConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]

        if self.user is not None:
            try:
                user = await OurUser.objects.aget(name=self.user.username)
                user.socket_ctr += 1
                await user.asave()
                await self.accept()
            except OurUser.DoesNotExist:
                pass

    async def disconnect(self, close_code):
        self.user = self.scope["user"]

        if self.user is not None:
            try:
                user = await OurUser.objects.aget(name=self.user.username)
                user.socket_ctr -= 1
                await user.asave()
            except OurUser.DoesNotExist:
                pass

    async def receive(self, text_data):
        pass