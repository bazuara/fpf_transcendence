from django.db import models
from social.models import User as OurUser

# Create your models here.
class Game(models.Model):
    GAME_MODES = [
        ("1", "1vs1"),
        ("2", "2vs2"),
        ("T", "Torneo")
    ]
    game_mode       = models.CharField(max_length=10, choices=GAME_MODES)
    game_id         = models.CharField(max_length=30, unique=True, primary_key=True) #should be base 10 code
    user1           = models.ForeignKey(OurUser, on_delete=models.CASCADE, related_name='games_user1')
    user1_connected = models.BooleanField(default=False)
    user2           = models.ForeignKey(OurUser, null=True, blank=True, on_delete=models.CASCADE, related_name='games_user2')
    user2_connected = models.BooleanField(default=False)
    user3           = models.ForeignKey(OurUser, on_delete=models.CASCADE, related_name='games_user3')
    user3_connected = models.BooleanField(default=False)
    user4           = models.ForeignKey(OurUser, null=True, blank=True, on_delete=models.CASCADE, related_name='games_user4')
    user4_connected = models.BooleanField(default=False)
    score1          = models.PositiveIntegerField(default = 0)
    score2          = models.PositiveIntegerField(default = 0)
    game_started    = models.BooleanField(default=False)
    end_time        = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.game_id} Team 1 {self.score1} / {self.score2} Team 2"

    class Meta:
        ordering = ['-end_time']