from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from users.forms import SignUpForm


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        sign_up_form = SignUpForm()
        ctx = {
            'sign_up_form': sign_up_form,
            'nav_section': 'home'
        }
        return render(request, 'home.html', ctx)


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class ChangeSiteView(View):
    def get(self, request):
        new_site = self.request.GET.get('site_id')
        request.session['site_id'] = new_site
        return HttpResponseRedirect(self.request.GET.get('next', '/'))
