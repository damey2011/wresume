import mimetypes

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from documents.models import Document
from home.views import TenantAccessPublicMixin


class DocumentPublicView(TenantAccessPublicMixin, View):
    def get(self, request, slug):
        doc = get_object_or_404(Document, slug=slug, user=self.request.tenant.user)
        file_mimetype = mimetypes.guess_type(doc.doc.path)
        response = HttpResponse(doc.doc, content_type=file_mimetype)
        response['Content-Disposition'] = 'attachment; filename=%s' % doc.doc.name
        return response
