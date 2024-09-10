from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=10, unique=True) #intra username
    alias        = models.CharField(max_length=10) #alias for tournaments
    wins         = models.PositiveIntegerField()
    loses        = models.PositiveIntegerField()
    friends      = models.ManyToManyField('self', symmetrical=False, blank=True) #friendlist
    avatar       = models.ImageField(upload_to ='uploads/', null=True, blank=True) #custom avatar
    intra_image  = models.URLField(max_length=512, null=True, blank=True) #used as default avatar if none is provided by user
    
    def __str__(self):
        return f"{self.id} {self.name} {self.wins}W/{self.loses}L/{self.games_played}T"

    @property
    def games_played(self):
        """Calculate total games played."""
        return self.wins + self.loses

    @property
    def win_ratio(self):
        """Calculate win ratio as a percentage."""
        if self.games_played == 0:
            return 0.0
        return round((self.wins / self.games_played) * 100.0, 2)

    class Meta:
        ordering = ['id']
