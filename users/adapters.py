import re

from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError
from django.urls import reverse


class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        return reverse('home:dashboard')

    def clean_username(self, username, shallow=False):
        if not re.match(r'^\w+_?$', username):
            raise ValidationError('Username cannot contain any special characters except \'_\'')
        return super(AccountAdapter, self).clean_username(username.lower(), shallow)
