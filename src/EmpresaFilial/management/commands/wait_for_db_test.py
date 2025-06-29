import os
import time
import psycopg2
from psycopg2 import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for test database...') 

        db_host = os.environ.get('TEST_DB_HOST')
        db_name = os.environ.get('TEST_DB_NAME')
        db_user = os.environ.get('TEST_DB_USER')
        db_password = os.environ.get('TEST_DB_PASSWORD')
        db_port = os.environ.get('TEST_DB_PORT', 5432)

        db_up = False
        while not db_up:
            try:
                conn = psycopg2.connect(
                    host=db_host,
                    dbname=db_name,
                    user=db_user,
                    password=db_password,
                    port=db_port
                )
                conn.close()
                db_up = True
            except (OperationalError, psycopg2.Error) as e:
                self.stdout.write(f'Test database unavailable ({e.__class__.__name__}), waiting 1 second...') 
                time.sleep(1)
        
        self.stdout.write(self.style.SUCCESS('Test database available!'))