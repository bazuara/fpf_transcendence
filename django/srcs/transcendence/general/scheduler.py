from apscheduler.schedulers.background import BackgroundScheduler

from social.anonymization import anonymize_inactive_users
from rooms.scheduler import delete_empty_rooms, delete_write_finished_tournaments
from game.views import delete_finished_games_dicts


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_finished_games_dicts, 'interval', minutes=5)
    scheduler.add_job(delete_empty_rooms, 'interval', minutes=5)
    scheduler.add_job(delete_write_finished_tournaments, 'interval', minutes=1)
    scheduler.add_job(anonymize_inactive_users, 'interval', days=1)
    scheduler.start()
 