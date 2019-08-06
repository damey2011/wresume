from django.core.management import BaseCommand

from users.models import SocialProfile, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            SocialProfile.objects.get_or_create(user=user)
