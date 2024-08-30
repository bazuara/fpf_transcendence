from django.db import models

class User(models.Model):
    user_id      = models.PositiveIntegerField(unique=True) #intra uid (maybe not needed)
    name         = models.CharField(max_length=10, unique=True) #intra username
    alias        = models.CharField(max_length=10) #alias for tournaments
    wins         = models.PositiveIntegerField()
    loses        = models.PositiveIntegerField()
    games_played = models.PositiveIntegerField()
    friends      = models.ManyToManyField('self', symmetrical=False, blank=True) #friendlist
    avatar       = models.ImageField(upload_to ='uploads/', null=True, blank=True) #custom avatar
    intra_image  = models.URLField(max_length=255) #used as default avatar if none is provided by user
    
    def __str__ (self):
        return f"{self.user_id} {self.name} {self.wins}W/{self.loses}L/{self.games_played}T"
    
    def win_ratio (self):
        if self.games_played == 0:
            return 0.0
        return (self.wins / self.games_played) * 100.0

    class Meta:
        ordering = ['user_id']
    

# Create your models here.
