from django.db.models.signals import post_save, post_delete

from users.models import User, Profile, SiteSettings, Client, SocialProfile
from wresume.utils import create_tenant
from PIL import Image as Img, ImageOps


def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        SocialProfile.objects.create(user=instance)
        create_tenant(instance)


def user_deleted(sender, instance, **kwargs):
    pass


def resize_uploaded_image(sender, instance, **kwargs):
    if instance.photo:
        img = Img.open(instance.photo.path)
        # Means it is a rectangular
        if img.width > img.height:
            if img.width <= 1000:
                pass
            elif img.width > 1000:
                # So as to maintain Aspect Ratio
                new_width = 1000
                new_height = ((new_width/img.width) * img.height)
                img = img.resize((int(new_width), int(new_height)))
                img.save(instance.photo.path, format="JPEG", quality=60)
            else:
                img.save(instance.photo.path, format="JPEG", quality=60)
        # square
        else:
            if img.height <= 1000:
                pass
            else:
                # So as to maintain Aspect Ratio
                new_height = 1000
                new_width = ((new_height / img.height) * img.width)
                size = (int(new_width), int(new_height))
                img.resize(size)
                bg_size = (1500, 1000)
                img = ImageOps.fit(img, bg_size, Img.ANTIALIAS, centering=(0.5, 0.5))
                img.save(instance.photo.path, format="JPEG", quality=60)


def create_client_settings(sender, instance, created, **kwargs):
    if created:
        SiteSettings.objects.create(client=instance)
        # call_command('migrate_schemas', executor='parallel')


post_save.connect(resize_uploaded_image, sender=User)
post_save.connect(user_created, sender=User)
post_save.connect(create_client_settings, sender=Client)
post_delete.connect(user_deleted, sender=User)
