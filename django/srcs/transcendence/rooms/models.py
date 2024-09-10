from django.db import models
from social.models import User as OurUser

class Room(models.Model):
	GAME_MODES = [
		("1", "1vs1"),
		("2", "2vs2"),
		("T", "Torneo")
	]
	game_mode = models.CharField(max_length=10, choices=GAME_MODES)
	user1	 = models.ForeignKey(OurUser, on_delete=models.PROTECT, null=True, blank=True, related_name='rooms_as_user1')
	user2	 = models.ForeignKey(OurUser, on_delete=models.PROTECT, null=True, blank=True, related_name='rooms_as_user2')
	user3	 = models.ForeignKey(OurUser, on_delete=models.PROTECT, null=True, blank=True, related_name='rooms_as_user3')
	user4	 = models.ForeignKey(OurUser, on_delete=models.PROTECT, null=True, blank=True, related_name='rooms_as_user4')
	room_id   = models.CharField(primary_key=True, max_length=6) #should be base 10 code #make primary key
	is_public = models.BooleanField(default=False)

	def __str__(self):
		return f"{self.room_id} {self.user1} {self.user2}"