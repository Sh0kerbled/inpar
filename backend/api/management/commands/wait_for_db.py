import time
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = 'Wait for database to be available'

    def handle(self, *args, **options):
        db_up = False
        retries = 30

        while not db_up and retries > 0:
            try:
                connection.ensure_connection()
                db_up = True
                self.stdout.write(self.style.SUCCESS('Database is ready!'))
            except OperationalError:
                retries -= 1
                self.stdout.write(f'Database unavailable, waiting... ({retries} retries left)')
                time.sleep(1)

        if not db_up:
            raise Exception('Database unavailable after 30 seconds')
