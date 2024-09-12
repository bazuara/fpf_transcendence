from django.contrib import admin
from rooms.models import Room

# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_id', 'game_mode', 'user1', 'user3', 'is_public', 'updated_at']
    search_fields = ['room_id']

admin.site.register(Room, RoomAdmin)