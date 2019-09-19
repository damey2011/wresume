from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from users.forms import SignUpForm, ContactDataForm
from users.views import BasicProfileView
from wresume.utils import generate_db_dump


class HomePageView(View):
    def ctx_data(self):
        sign_up_form = SignUpForm()
        contact_form = ContactDataForm(initial={'client': self.request.tenant.id})
        ctx = {
            'sign_up_form': sign_up_form,
            'nav_section': 'home',
            'contact_form': contact_form
        }
        return ctx

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home:dashboard'))
        return render(request, 'home.html', self.ctx_data())

    def post(self, request, *args, **kwargs):
        form = ContactDataForm(self.request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your contact form has been sent successfully', 'success')
            return HttpResponseRedirect('/')
        if 'is_ajax' in request.POST:
            return JsonResponse(form.errors, status=400)
        return render(request, 'home.html', self.ctx_data())


class DashboardView(BasicProfileView):
    pass


class ChangeSiteView(View):
    def get(self, request):
        new_site = self.request.GET.get('site_id')
        request.session['site_id'] = new_site
        return HttpResponseRedirect(self.request.GET.get('next', '/'))
