import os
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.contrib.auth import get_user_model

class Command(createsuperuser.Command):
    help = 'Create a superuser with password provided from environment variables.'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--password', dest='password', default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        password = options.get('password')
        database = options.get('database')

        UserModel = get_user_model()

        if UserModel.objects.filter(username=username).exists():
            print(f"User '{username}' already exists. Superuser creation skipped.")
            return

        super(Command, self).handle(*args, **options)

        if password:
            user = self.UserModel._default_manager.db_manager(database).get(username=username)
            user.set_password(password)
            user.save()
            print(f"Password set for user: {username}")
