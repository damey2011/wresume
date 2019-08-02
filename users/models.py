from django.contrib.auth.models import AbstractUser
from django.db import models
from tenant_schemas.models import TenantMixin


class User(AbstractUser):

    def __str__(self):
        return self.username


class Client(TenantMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    auto_create_schema = True

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    city = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username
