from django.contrib import admin
from rooms.models import Room, Tournament

# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'game_mode', 'user1', 'user3', 'is_public', 'updated_at']
    search_fields = ['room_id']

class TournamentAdmin(admin.ModelAdmin):
    list_display = ['tournament_id', 'user1', 'user2', 'user3', 'user4']
    search_fields = ['tournament_id']

admin.site.register(Room, RoomAdmin)
admin.site.register(Tournament, TournamentAdmin)
