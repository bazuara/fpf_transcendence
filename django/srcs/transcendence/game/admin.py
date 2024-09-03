from django.contrib import admin
from game.models import Game

# Register your models here.

class GameAdmin(admin.ModelAdmin):
    list_display = ['game_id', 'user1', 'user2', 'mode_one_vs_one']
    search_fields = ['game_id']

admin.site.register(Game, GameAdmin)
