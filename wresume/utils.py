import os
from urllib.parse import urljoin

from django import forms
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.utils.encoding import filepath_to_uri
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import FormView
from selenium import webdriver
from tenant_schemas.storage import TenantStorageMixin

from users.models import Client
from wresume import settings


def create_tenant(user):
    domain_url = get_site() if user.username == 'admin' else f'{user.username}.{get_site()}'
    schema_name = settings.PUBLIC_SCHEMA_NAME if user.username is 'admin' else user.username
    client = Client(domain_url=domain_url, schema_name=schema_name, user=user)
    client.save()
    return client


def get_tenant(user):
    return Client.objects.get(user=user)


def get_site():
    return settings.SITE_DOMAIN


def get_absolute_site():
    if settings.DEBUG:
        return 'http://' + get_site()
    return 'https://' + get_site()


def get_default_user_password():
    return settings.DEFAULT_USER_PASSWORD


def is_public(request):
    return request.tenant.schema_name == settings.PUBLIC_SCHEMA_NAME


def reverse_absolute(site, path):
    protocol = 'https://'
    if 'localhost' in site.domain_url:
        protocol = 'http://'
    return protocol + site.domain_url + path


def take_screenshot(url):
    driver = webdriver.Chrome('chromedriver')
    driver.get(url)
    screenshot = driver.get_screenshot_as_png()
    driver.quit()
    return SimpleUploadedFile('screenshot.png', screenshot, content_type='image/png')


def media_absolute_uri(request, media_url):
    if 'http' not in media_url:
        return request.build_absolute_uri(media_url)
    return media_url


def get_absolute_url(path):
    domain = Site.objects.get_current().domain
    if 'localhost' in domain:
        return 'http://' + domain + path
    return 'https://' + domain + path


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        fields = self.fields
        for field in fields.keys():
            current_field = fields[field]
            current_field.widget.attrs.update({'class': 'form-control'})
            if hasattr(self.Meta, 'labels'):
                current_field.widget.attrs.update({'placeholder': self.Meta.labels.get(field)})
            if isinstance(fields[field].widget, forms.Select):
                current_field.widget.choices[0] = ('', self.Meta.labels.get(field))
            # Add the required asterick
            if current_field.widget.is_required and current_field.label:
                current_field.label = mark_safe(current_field.label + '<span class="text-danger">*</span>')


class SiteAwareView:
    site = None

    def get_site(self):
        if self.request.GET.get('site'):
            self.request.session['site_id'] = self.request.GET.get('site')
            return self.request.user.client_set.get(pk=int(self.request.GET.get('site')))
        if self.request.session.get('site_id'):
            return self.request.user.client_set.get(pk=int(self.request.session['site_id']))
        site_object = self.request.user.client_set.first()
        self.request.session['site_id'] = site_object.id
        return site_object

    def get_context_data(self, **kwargs):
        ctx = super(SiteAwareView, self).get_context_data(**kwargs)
        ctx['sites'] = self.request.user.client_set.all()
        ctx['selected_site'] = self.get_site().id
        return ctx


class MyFileStorage(TenantStorageMixin, FileSystemStorage):
    def url(self, name):
        if self.base_url is None:
            raise ValueError("This file is not accessible via a URL.")
        name = os.path.join(connection.tenant.domain_url, name)
        url = filepath_to_uri(name)
        if url is not None:
            url = url.lstrip('/')
        return urljoin(self.base_url, url)
