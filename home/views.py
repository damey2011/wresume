from django.conf import settings
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from resumes.models import SiteTemplate
from users.models import Client


class TenantAccessPublicMixin:
    def dispatch(self, request, *args, **kwargs):
        connection.set_tenant(Client.objects.get(schema_name=settings.PUBLIC_SCHEMA_NAME))
        return super(TenantAccessPublicMixin, self).dispatch(request, *args, **kwargs)


class TenantHomeView(TenantAccessPublicMixin, View):
    def get(self, request, *args, **kwargs):
        content = get_object_or_404(SiteTemplate, site=self.request.tenant).template.construct_page()
        return HttpResponse(content)
