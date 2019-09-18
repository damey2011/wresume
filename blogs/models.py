from html import escape

import requests
from bs4 import BeautifulSoup
from django.core.files.uploadedfile import SimpleUploadedFile
from django.templatetags.static import static

from users.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image as Img, ImageOps
from django.template.defaultfilters import slugify
from django.urls import reverse
from model_utils.models import TimeStampedModel, SoftDeletableModel
from users.models import Client
from wresume.utils import reverse_absolute


class BlogCategory(TimeStampedModel):
    category = models.CharField(max_length=100)
    site = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['category', 'site']

    def __str__(self):
        return self.category


class BlogPost(SoftDeletableModel, TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    slug = models.CharField(blank=True, max_length=150)
    image = models.ImageField(upload_to='post-header-images', blank=True, null=True)
    category = models.ForeignKey(to=BlogCategory, null=True, on_delete=models.CASCADE)
    seo_desc = models.TextField(blank=True)
    seo_keywords = models.CharField(max_length=100, blank=True)
    post_image = models.ImageField(upload_to='blog-post-headers', blank=True, null=True)
    views = models.IntegerField(default=0)
    site = models.ForeignKey(Client, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:100]
        if not self.image:
            # If no image is provided, pick from the content if available
            soup = BeautifulSoup(self.content, 'html.parser')
            images = soup.find_all('img')
            if len(images):
                url = images[0]['src']
                # download the object
                resp = requests.get(url)
                file = SimpleUploadedFile(self.title[:10], resp.content, resp.headers['content-type'])
                self.image = file
        super(BlogPost, self).save(*args, **kwargs)

    def previous_post(self):
        qs = BlogPost.objects.filter(id__lt=self.id, site=self.site)
        if qs.exists():
            return qs.last()
        return None

    def next_post(self):
        qs = BlogPost.objects.filter(id__gt=self.id, site=self.site)
        if qs.exists():
            return qs.first()
        return None

    def get_absolute_url(self):
        return reverse_absolute(self.site,
                                reverse('blogs:blog-post', kwargs={'slug': self.slug}, urlconf='wresume.urls'))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class Comment(SoftDeletableModel, TimeStampedModel):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content[:25]

    class Meta:
        ordering = ['-created']

    @property
    def escaped_content(self):
        return escape(self.content)


@receiver(post_save, sender=BlogPost)
def resize_uploaded_image(sender, instance, **kwargs):
    if instance.image:
        img = Img.open(instance.image.path)
        # Means it is a rectangular
        if img.width > img.height:
            if img.width <= 1000:
                pass
            elif img.width > 1000:
                # So as to maintain Aspect Ratio
                new_width = 1000
                new_height = ((new_width / img.width) * img.height)
                img = img.resize((int(new_width), int(new_height)))
                img.save(instance.image.path, format="JPEG", quality=60)
            else:
                img.save(instance.image.path, format="JPEG", quality=60)
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
                img.save(instance.image.path, format="JPEG", quality=60)


class BlogImage(models.Model):
    image = models.ImageField(upload_to='blog/images')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class Template(SoftDeletableModel, TimeStampedModel):
    name = models.CharField(max_length=200)
    screenshot = models.ImageField(upload_to='templates/screenshots/', null=True)
    template_folder = models.CharField(max_length=1000, default='')

    def __str__(self):
        return self.template_folder

    def get_screenshot_url(self):
        if self.template_folder:
            return self.screenshot.__str__()
        if self.screenshot:
            return self.screenshot.url
        return static('images/new-images/noimage.png')


class SiteBlogTemplate(TimeStampedModel):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.client.schema_name}-{self.template.template_folder}'
