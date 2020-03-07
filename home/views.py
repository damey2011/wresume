from django.conf import settings
from django.contrib import messages
from django.db import connection
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from resumes.models import SiteTemplate, Template
from users.forms import ContactDataForm
from users.models import Client


class TenantAccessPublicMixin:
    def dispatch(self, request, *args, **kwargs):
        connection.set_tenant(Client.objects.get(schema_name=settings.PUBLIC_SCHEMA_NAME))
        if self.request.tenant.sitesettings.enable_site:
            return super(TenantAccessPublicMixin, self).dispatch(request, *args, **kwargs)
        return HttpResponse('<h1>Please check back later.</h1><div>Site is currently disabled, If your email is '
                            'verified and you didn\'t perform this action on your own, please send an email '
                            'to heyo@wresu.me.</div>')


class TenantHomeView(TenantAccessPublicMixin, View):
    def get_response(self, context):
        template = self.get_template_page()
        if template.template_path:
            return render(self.request, template.template_path, context)
        return HttpResponse(template.construct_page())

    def get_template_page(self):
        slug = self.kwargs.get('slug')
        if slug:
            return get_object_or_404(Template, slug=slug)
        return get_object_or_404(SiteTemplate, site=self.request.tenant).template

    def get(self, request, *args, **kwargs):
        ctx = dict()
        ctx['contact_form'] = ContactDataForm(initial={'client': self.request.tenant.id})
        return self.get_response(ctx)

    def post(self, request, *args, **kwargs):
        form = ContactDataForm(self.request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your contact form has been sent successfully', 'success')
            return HttpResponseRedirect('/')
        if 'is_ajax' in request.POST:
            return JsonResponse(form.errors, status=400)
        return self.get_response({'contact_form': form})


def test(request):
    return render(request, 'stock/bulma-light/index.html')
