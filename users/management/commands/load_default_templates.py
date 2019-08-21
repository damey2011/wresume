from django.core.management import BaseCommand
from django.db import connection

from resumes.constants import STOCK_TEMPLATES
from resumes.models import Template


class Command(BaseCommand):
    def handle(self, *args, **options):
        if connection.alias == 'default':
            for template in STOCK_TEMPLATES:
                Template.objects.get_or_create(**template)
