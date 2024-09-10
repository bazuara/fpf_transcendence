import json
import io

from channels.generic.websocket import WebsocketConsumer
from .models import Room
from social.models import User as OurUser
from asgiref.sync import async_to_sync
#handle errors
#handle locks
#handle user already in room
class RoomConsumer(WebsocketConsumer):

	def connect(self):
		self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
		self.group_name = "room_" + self.room_id
		room = Room.objects.get(room_id=self.room_id)
		self.user = self.scope["user"]

		if not room or not self.user:
			return

		ourUser = OurUser.objects.get(name=self.user.username)

		if room.user1 is None:
			room.user1 = ourUser
		elif room.game_mode == "1":
			if room.user3 is None:
				room.user3 = ourUser
			else:
				pass #think about reject
		else:
			if room.user2 is None:
				room.user2 = ourUser
			elif room.user3 is None:
				room.user3 = ourUser
			elif room.user4 is None:
				room.user4 = ourUser
			else:
				pass #think about reject

		room.save()

		async_to_sync(self.channel_layer.group_add) (self.group_name, self.channel_name)
		self.accept()
		async_to_sync(self.channel_layer.group_send) (self.group_name, {"type": "state.update"})

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard) (self.group_name, self.channel_name)

	def state_update(self, event):
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

	def receive(self, text_data):
		self.send(text_data)
