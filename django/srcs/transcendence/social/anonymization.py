import random, string
from social.models import User as OurUser
from django.contrib.sessions.models import Session
from datetime import timedelta
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(anonymize_inactive_users, 'interval', minutes=10)
    scheduler.start()

def anonymize_inactive_users():
    print("Anonymize Inactive Users")
    time_now = timezone.now()
    all_users = OurUser.objects.filter(anonymized=False, socket_ctr=0)
    for user in all_users:
        if (time_now - user.updated_at) > timedelta(hours=1):
            print(f"deleting: {user}")
            clear_user_data(user)

def clear_user_data(user):
    def generate_random_string_with_uppercase():
        uppercase_letter = random.choice(string.ascii_uppercase)
        remaining_characters = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
        random_position = random.randint(0, 9)
        random_text = remaining_characters[:random_position] + uppercase_letter + remaining_characters[random_position:]
        return random_text

    def gen_random_name():
        random_text = generate_random_string_with_uppercase()
        user = OurUser.objects.filter(name=random_text).first()
        if not user:
            return random_text
        else:
            gen_random_name()

    # Delete avatar and intra_image
    if user.avatar:
        user.avatar.delete()
        user.avatar = None
    user.intra_image = None
    # Set new_name and new_alias
    new_name = gen_random_name()
    user.name = new_name
    user.alias = new_name
    # Set anonymized flag to true so routine of anonymize_inactive_users() skips already anonymized users
    user.anonymized = True
    # Delete anonymized user from all the users friendlists
    users_with_user_as_friend = OurUser.objects.filter(friends=user)
    for foreign_user in users_with_user_as_friend:
        foreign_user.friends.remove(user)
    # Delete anonymized user friends
    user.friends.clear()
    # Save
    user.save()
