from django.db.models.signals import post_save, post_delete

from users.models import User, Profile
from wresume.utils import create_tenant, get_tenant


def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        create_tenant(instance)


def user_deleted(sender, instance, **kwargs):
    get_tenant(instance).delete()


post_save.connect(user_created, sender=User)
post_delete.connect(user_deleted, sender=User)
