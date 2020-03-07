import mimetypes

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View

from documents.models import Document
from home.views import TenantAccessPublicMixin


class DocumentPublicView(TenantAccessPublicMixin, View):
    def get(self, request, slug):
        doc = get_object_or_404(Document, slug=slug, user=self.request.tenant.user)
        return HttpResponseRedirect(doc.get_absolute_url)
