import mimetypes

from django.core.management import call_command
from django.db.models.signals import post_save, post_delete

from resumes.constants import STOCK_TEMPLATES
from resumes.models import SiteTemplate, Template
from blogs.models import SiteBlogTemplate, Template as BlogTemplate
from users.management.commands.load_blog_templates import BLOG_TEMPLATES
from users.models import User, Profile, SiteSettings, Client, SocialProfile
from wresume.utils import create_tenant, get_tenant
from PIL import Image as Img, ImageOps


def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        SocialProfile.objects.create(user=instance)
        create_tenant(instance)


def user_deleted(sender, instance, **kwargs):
    pass


def resize_uploaded_image(sender, instance, **kwargs):
    try:
        file_format = mimetypes.guess_type(instance.photo.path)[1]
    except Exception as e:
        file_format = 'JPEG'
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
                img.save(instance.photo.path, format=file_format, quality=60)
            else:
                img.save(instance.photo.path, format=file_format, quality=60)
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
                img.save(instance.photo.path, format=file_format, quality=60)


def create_client_settings(sender, instance, created, **kwargs):
    if created:
        # Settle Default Site Template
        SiteSettings.objects.create(client=instance)
        templates = Template.objects.filter(name='CV Portfolio')
        if templates.exists():
            SiteTemplate.objects.create(template=templates.first(), site=instance)
        else:
            if len(STOCK_TEMPLATES):
                call_command('load_default_templates')
                SiteTemplate.objects.create(template=templates.first(), site=instance)
        # Settle Default Blog Template
        blog_templates = BlogTemplate.objects.filter(name='Eden')
        if blog_templates.exists():
            SiteBlogTemplate.objects.create(template=blog_templates.first(), client=instance)
        else:
            if len(BLOG_TEMPLATES):
                call_command('load_blog_templates')
                SiteBlogTemplate.objects.create(template=blog_templates.first(), client=instance)


post_save.connect(resize_uploaded_image, sender=User)
post_save.connect(user_created, sender=User)
post_save.connect(create_client_settings, sender=Client)
post_delete.connect(user_deleted, sender=User)
