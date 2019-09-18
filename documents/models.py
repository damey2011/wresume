import os

from django.db import models
from django.urls import reverse

from django.utils.text import slugify
from model_utils.models import SoftDeletableModel, TimeStampedModel

from users.models import User
from wresume.utils import get_absolute_url, random_string, get_tenant, get_tenant_url


def docs_upload_to(instance, filename):
    return os.path.join('docs', instance.user.username, filename)


class Document(SoftDeletableModel, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    doc = models.FileField(upload_to=docs_upload_to)
    description = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField()

    def __str__(self):
        return f'{self.title} - {round(self.doc.size/1000, 2)}kb'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            while self.__class__.objects.filter(slug=self.slug).exists():
                self.slug = slugify(self.title + random_string(5))
        super(Document, self).save(*args, **kwargs)

    @property
    def public_url(self):
        return get_tenant_url(get_tenant(self.user)) + reverse(
            'docs:shareable-view', args=[self.slug], urlconf='wresume.urls')

    @property
    def edit_url(self):
        return reverse('docs_public:edit', kwargs={'slug': self.slug})

    @property
    def delete_url(self):
        return reverse('docs_public:delete', kwargs={'slug': self.slug})