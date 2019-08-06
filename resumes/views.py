from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.translation import ugettext as __
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from rest_framework import status

from resumes.forms import CreateTemplateForm
from resumes.models import Template, TemplateAsset, SiteTemplate
from wresume.utils import SiteAwareView, media_absolute_uri


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        pass


class ListTemplatesView(LoginRequiredMixin, SiteAwareView, ListView):
    extra_context = {'nav_section': 'page', 'is_templates': True}

    def get_queryset(self):
        return Template.objects.filter(owner=self.request.user, is_public=True)

    template_name = 'resumes/list.html'


class ListMyTemplatesView(LoginRequiredMixin, SiteAwareView, ListView):
    extra_context = {'nav_section': 'page', 'is_my_templates': True}
    context_object_name = 'templates'
    template_name = 'resumes/my-templates.html'
    paginate_by = 10

    def get_queryset(self):
        return Template.objects.filter(owner=self.request.user, is_public=False)


class PreviewMyTemplateView(DetailView):
    extra_context = {'nav_section': 'page', 'is_my_templates': True}
    template_name = 'resumes/construct_template.html'

    def get_queryset(self):
        return Template.objects.filter(is_public=False)

    def get_context_data(self, **kwargs):
        ctx = super(PreviewMyTemplateView, self).get_context_data(**kwargs)
        ctx['content'] = self.get_object().content
        ctx['styles'] = self.get_object().styles
        ctx['js'] = self.get_object().js
        ctx['title'] = self.get_object().name
        return ctx

    def get(self, request, *args, **kwargs):
        if request.GET.get('json'):
            response = {
                'gjs-components': self.get_object().gjs_components,
                'gjs-html': self.get_object().content,
                'gjs-styles': self.get_object().styles,
                'gjs-js': self.get_object().js,
            }
            return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
        return super(PreviewMyTemplateView, self).get(request, *args, **kwargs)


class MyTemplateActivateView(SiteAwareView, View):
    def get(self, request, pk, **kwargs):
        SiteTemplate.objects.filter(site=self.get_site()).delete()
        SiteTemplate.objects.create(template_id=pk, site=self.get_site())
        template = get_object_or_404(Template, pk=pk)
        messages.success(request, __('%(temp)s is now active for %(site)s') % {'temp': template.name,
                                                                               'site': self.get_site().domain_url})
        return HttpResponseRedirect(request.GET.get('next', reverse('resumes:my-templates')))


class MyTemplateDeactivateView(SiteAwareView, View):
    def get(self, request, pk, **kwargs):
        SiteTemplate.objects.filter(site=self.get_site(), template_id=pk).delete()
        template = get_object_or_404(Template, pk=pk)
        messages.success(request, __('%(temp)s has been deactivated for %(site)s') % {
            'temp': template.name, 'site': self.get_site().domain_url})
        return HttpResponseRedirect(request.GET.get('next', reverse('resumes:my-templates')))


class MyTemplateDeleteView(SiteAwareView, View):
    def get(self, request, pk, **kwargs):
        template = get_object_or_404(Template, pk=pk)
        messages.success(request, __('%(temp)s has been deleted') % {'temp': template.name})
        template.delete()
        return HttpResponseRedirect(request.GET.get('next', reverse('resumes:my-templates')))


class CreateTemplateView(LoginRequiredMixin, SuccessMessageMixin, SiteAwareView, CreateView):
    template_name = 'resumes/create-template.html'
    extra_context = {'nav_section': 'page', 'fullwidth': True, 'is_create_template': True}
    form_class = CreateTemplateForm
    success_url = reverse_lazy('resumes:my-templates')

    def get_success_message(self, cleaned_data):
        return __('{} has been saved'.format(cleaned_data['name']))

    def get_initial(self):
        init = super(CreateTemplateView, self).get_initial()
        init['owner'] = self.request.user.id
        init['content'] = ''
        return init

    def get_queryset(self):
        return Template.objects.filter(owner=self.request.user, is_public=False)

    def get_context_data(self, **kwargs):
        ctx = super(CreateTemplateView, self).get_context_data(**kwargs)
        ctx['user_assets'] = [media_absolute_uri(self.request, ta.asset.url) for ta in TemplateAsset.objects.filter(
            user=self.request.user)]
        return ctx


class UpdateMyTemplateView(SuccessMessageMixin, UpdateView):
    extra_context = {'nav_section': 'page', 'fullwidth': True, 'is_editing_template': True}
    template_name = 'resumes/update-template.html'
    success_url = reverse_lazy('resumes:my-templates')
    context_object_name = 'template'
    form_class = CreateTemplateForm

    def get_success_message(self, cleaned_data):
        return __('{} has been updated'.format(cleaned_data['name']))

    def get_queryset(self):
        return Template.objects.filter(is_public=False)

    def get_context_data(self, **kwargs):
        ctx = super(UpdateMyTemplateView, self).get_context_data(**kwargs)
        ctx['user_assets'] = [media_absolute_uri(self.request, ta.asset.url) for ta in TemplateAsset.objects.filter(
            user=self.request.user)]
        return ctx


class GJSUploadView(View):
    def post(self, request, user, **kwargs):
        files = self.request.FILES.getlist('files') or self.request.FILES.getlist('files[]')
        urls = []
        for file in files:
            urls.append(TemplateAsset.objects.create(user_id=user, asset=file).asset.url)
        return JsonResponse({'data': urls}, status=201)

    def get(self, request, user, **kwargs):
        return JsonResponse(TemplateAsset.objects.filter(user_id=user).values_list('asset', flat=True), status=200)
