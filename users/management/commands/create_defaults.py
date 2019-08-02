from django.core.management import BaseCommand
from django.db import connection

from users.models import User

from wresume.utils import get_default_user_password, get_site


class Command(BaseCommand):
    def handle(self, *args, **options):
        if connection.alias == 'default':
            User.objects.create_superuser(username='admin', email='admin@localhost.com',
                                          password=get_default_user_password())
