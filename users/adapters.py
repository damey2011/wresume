from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        return reverse('home:dashboard')
