from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Resync the sequences of the UserProfile table'

    def handle(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval(pg_get_serial_sequence('users_userprofile', 'id'), COALESCE(MAX(id), 1), MAX(id) IS NOT NULL) FROM users_userprofile")
            self.stdout.write(self.style.SUCCESS('Successfully resynced UserProfile sequence'))