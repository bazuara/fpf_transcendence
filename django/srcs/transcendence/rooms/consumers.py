import json
import io
import threading

from channels.generic.websocket import WebsocketConsumer
from .models import Room
from social.models import User as OurUser
from asgiref.sync import async_to_sync

lock_dict = {}
global_dict_lock = threading.Lock()

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
		except:
			return
		finally:
			release_lock(self.room_id)

		room.save()

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
				case room.user2:
					room.user2 = None
				case room.user3:
					room.user3 = None
				case room.user4:
					room.user4 = None
				case _:
					pass
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
