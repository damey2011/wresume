from django.core.management import BaseCommand
from django.db import connection

from resumes.models import Template


class Command(BaseCommand):
    def handle(self, *args, **options):
        if connection.alias == 'default':
            Template.objects.create(is_public=True, name='Wresume Default',
                                    screenshot='stock/jackson-colorlib/images/homescreenshot.png',
                                    template_path='stock/jackson-colorlib/index.html')
