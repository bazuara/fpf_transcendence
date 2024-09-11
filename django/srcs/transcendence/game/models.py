from django.db import models
from social.models import User as OurUser

# Create your models here.
class Game(models.Model):
    game_id         = models.CharField(max_length=30, unique=True, primary_key=True) #should be base 10 code
    user1           = models.ForeignKey(OurUser, on_delete=models.CASCADE, related_name='games_user1')
    user2           = models.ForeignKey(OurUser, null=True, blank=True, on_delete=models.CASCADE, related_name='games_user2')
    user3           = models.ForeignKey(OurUser, on_delete=models.CASCADE, related_name='games_user3')
    user4           = models.ForeignKey(OurUser, null=True, blank=True, on_delete=models.CASCADE, related_name='games_user4')
    score1          = models.PositiveIntegerField(default = 0)
    score2          = models.PositiveIntegerField(default = 0)
    end_time        = models.DateField(null=True)
    
    def __str__(self):
        return f"{self.game_id} Team 1 {self.score1} / {self.score2} Team 2"

    class Meta:
        ordering = ['game_id']