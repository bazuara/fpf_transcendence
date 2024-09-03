from django.db import models
from social.models import User

class Room(models.Model):
	GAME_MODES = [
        ("1", "1vs1"),
        ("2", "2vs2"),
        ("T", "Torneo")
    ]
	game_mode = models.CharField(max_length=10, choices=GAME_MODES)
	user1     = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='room_as_user_1')
	user2     = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='room_as_user_2')
	user3     = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='room_as_user_3')
	user4     = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name='room_as_user_4')
	room_id   = models.CharField(max_length=6, unique=True) #should be base 32 code
	is_public = models.BooleanField(default=False)