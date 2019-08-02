from users.models import Client
from wresume import settings


def create_tenant(user):
    domain_url = f'{user.username}.{get_site()}' if user.username == 'admin' else get_site()
    client = Client(domain_url=domain_url, schema_name=user.username, user=user)
    client.save()
    return client


def get_tenant(user):
    return Client.objects.get(user=user)


def get_site():
    return settings.SITE_DOMAIN


def get_default_user_password():
    return settings.DEFAULT_USER_PASSWORD
