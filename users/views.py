from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext as __
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, UpdateView

from users.forms import UserForm, SettingsForm, ResumeForm, SocialForm, EducationForm
from users.models import SiteSettings, EducationProfile
from wresume.utils import SiteAwareView


class BasicProfileView(UpdateView):
    template_name = 'dashboard/basic.html'
    extra_context = {'basic_tab': True, 'form_title': _('Edit Basic Details')}
    form_class = UserForm

    def get_success_url(self):
        return reverse('users:basic_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, __('Your profile has been updated successfully'))
        return super(BasicProfileView, self).form_valid(form)


class ResumeFormView(UpdateView):
    template_name = 'dashboard/profile.html'
    extra_context = {'resume_tab': True, 'form_title': _('Profile Details')}
    form_class = ResumeForm

    def form_valid(self, form):
        messages.success(self.request, __('Your profile has been updated successfully'))
        return super(ResumeFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:resume')

    def get_object(self, queryset=None):
        return self.request.user.profile


class SocialFormView(UpdateView):
    template_name = 'dashboard/profile.html'
    extra_context = {'social_tab': True, 'form_title': _('Social Details')}
    form_class = SocialForm

    def form_valid(self, form):
        messages.success(self.request, __('Your social profile has been updated successfully'))
        return super(SocialFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:social')

    def get_object(self, queryset=None):
        return self.request.user.socialprofile


class SettingsView(SiteAwareView, UpdateView):
    template_name = 'dashboard/site-settings.html'
    extra_context = {'settings_tab': True}
    form_class = SettingsForm
    success_url = reverse_lazy('users:settings')

    def get_object(self, queryset=None):
        site = self.get_site()
        settings, created = SiteSettings.objects.get_or_create(client=site)
        return settings

    def get_context_data(self, **kwargs):
        ctx = super(SettingsView, self).get_context_data(**kwargs)
        ctx['form_title'] = _('%(site)s Site Settings') % {'site': self.get_object().client.domain_url}
        return ctx

    def form_valid(self, form):
        messages.success(self.request, __('Your profile has been updated successfully'))
        return super(SettingsView, self).form_valid(form)


class MultiEntryView(SiteAwareView, FormView):
    template_name = 'dashboard/multi-entries-form.html'
    extra_context = {'settings_tab': True}
    form_class = EducationForm
    form_title = _('Add Education Entry')
    success_message = _('Your profile has been updated successfully')
    success_url = reverse_lazy('resumes:education')
    inject_initial = []
    object_list_filter = ['user']
    model = None

    def get_object_list(self):
        assert self.model is not None, 'Please provide model class'
        ol = self.model.objects.all()
        if 'user' in self.object_list_filter:
            ol = ol.filter(user=self.request.user)
        if 'site' in self.object_list_filter:
            ol = ol.filter(site=self.get_site())
        return ol

    def get_initial(self):
        init = super(MultiEntryView, self).get_initial()
        if 'user' in self.inject_initial:
            init['user'] = self.request.user.id
        if 'site' in self.inject_initial:
            init['site'] = self.get_site().id
        return init

    def get_context_data(self, **kwargs):
        ctx = super(MultiEntryView, self).get_context_data(**kwargs)
        ctx['form_title'] = self.form_title
        ctx['object_list'] = self.get_object_list()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        form.save()
        return super(MultiEntryView, self).form_valid(form)


class MultiEntryUpdateView(MultiEntryView, UpdateView):
    form_title = _('Update Education Entry')

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs.get('pk'))


class MultiEntryDeleteView(MultiEntryUpdateView):
    def get(self, request, *args, **kwargs):
        self.get_object().delete()
        return HttpResponseRedirect(request.GET.get('next', self.get_success_url()))

