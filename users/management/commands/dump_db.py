from django.core.management import BaseCommand

from resumes.models import DBDumps
from wresume.utils import generate_db_dump


class Command(BaseCommand):
    def handle(self, *args, **options):
        file = generate_db_dump()
        DBDumps.objects.create(file=file)
        print('Done')
