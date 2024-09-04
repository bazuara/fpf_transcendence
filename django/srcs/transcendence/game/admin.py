from django.contrib import admin
from game.models import Game

# Register your models here.

class GameAdmin(admin.ModelAdmin):
    list_display = ['game_id', 'user1', 'user3']
    search_fields = ['game_id']

admin.site.register(Game, GameAdmin)
