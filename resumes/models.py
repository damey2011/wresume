import os

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from model_utils.models import SoftDeletableModel, TimeStampedModel

from users.models import User, Client
from wresume.utils import take_screenshot, get_absolute_url


class Template(SoftDeletableModel, TimeStampedModel):
    gjs_components = JSONField(default=dict)
    content = models.TextField(blank=True, null=True)
    styles = models.TextField(default='', blank=True, null=True)
    js = models.TextField(default='', blank=True, null=True)
    name = models.CharField(max_length=100)
    screenshot = models.ImageField(upload_to='templates/screenshots/', null=True)
    template_path = models.CharField(max_length=1000, default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def construct_page(self):
        return render_to_string('resumes/construct_template.html', context={'js': self.js, 'content': self.content,
                                                                            'title': self.name, 'styles': self.styles})

    def get_screenshot_url(self):
        if self.template_path:
            return static(self.screenshot.__str__())
        if self.screenshot:
            return self.screenshot.url
        return static('images/new-images/noimage.png')

    def get_default_template_path(self):
        # This path will go to the one that has not been edited, hence they can see what the template is gonna look
        # like
        return self.template_path.replace('.html', '.default.html')

    def save(self, **kwargs):
        final_save = kwargs.pop('final_save', None)
        super(Template, self).save(**kwargs)
        # Only take screenshot of custom built pages
        if not final_save and not self.template_path:
            # To avoid endless loop
            self.screenshot = take_screenshot(get_absolute_url(reverse('resumes:my-template-preview',
                                                                       kwargs={'pk': self.id})))
            self.save(final_save=True)


class SiteTemplate(models.Model):
    site = models.OneToOneField(Client, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.site.domain_url + '->' + self.template.name


def get_asset_upload_to(instance, filename):
    return os.path.join('template-assets', instance.user.username, filename)


class TemplateAsset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.FileField(upload_to=get_asset_upload_to)

    def __str__(self):
        return self.user.username


class ContactFormData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=500, null=True, blank=True)
    message = models.TextField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
