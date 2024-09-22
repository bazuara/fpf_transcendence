from django.core.management.base import BaseCommand
from social.models import User as OurUser
from rooms.models import Room

class Command(BaseCommand):
    help = 'Restore socket_ctr to one on all users and remove all rooms'

    def handle(self, *args, **kwargs):
        print("\033[93mExecuting reset_user_sockets_and_clear_rooms!\033[0m")
        print("Setting all socket_ctr to 0...")
        OurUser.objects.all().update(socket_ctr=0)  
        print("Deleting rooms...")
        Room.objects.all().delete()
        print("\033[92mTask complete!\033[0m")
