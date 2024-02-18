"""
Django command will wait for the database to available.
"""

import time

from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from psycopg2 import OperationalError as psycopg2Error


class Command(BaseCommand):
    """Django command wait for database."""

    def handle(self, *args, **options):
        '''Entry points for command'''
        self.stdout.write('waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (psycopg2Error, OperationalError):
                self.stdout.write('database unavailabe, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('database available!'))
