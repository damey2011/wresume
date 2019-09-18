import os

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel, SoftDeletableModel
from tenant_schemas.models import TenantMixin


def profile_photo_upload_to(instance, filename):
    return os.path.join('profile_images', instance.username, filename)


def full_profile_photo_upload_to(instance, filename):
    return os.path.join('full_profile_images', instance.username, filename)


class User(AbstractUser):
    photo = models.ImageField(upload_to=profile_photo_upload_to, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    full_photo = models.ImageField(upload_to=full_profile_photo_upload_to, null=True, blank=True)

    def __str__(self):
        return self.username

    def home_url(self):
        from wresume.utils import get_tenant, get_tenant_url
        return get_tenant_url(get_tenant(self)) + reverse('home:tenant_home', urlconf='wresume.urls')

    def blogs_url(self):
        from wresume.utils import get_tenant, get_tenant_url
        return get_tenant_url(get_tenant(self)) + reverse('blogs:blog-post-list', urlconf='wresume.urls')


class Client(TenantMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    auto_create_schema = True

    def __str__(self):
        return self.user.username


class Profile(SoftDeletableModel):
    user = models.OneToOneField(User, models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


def site_settings_user_aware_upload_to(instance, filename):
    return os.path.join(instance.client.domain_url, 'favicons', filename)


class SiteSettings(models.Model):
    favicon = models.ImageField(upload_to=site_settings_user_aware_upload_to, null=True, blank=True)
    logo = models.ImageField(upload_to=site_settings_user_aware_upload_to, null=True, blank=True)
    primary_color = models.CharField(max_length=100, default='#557A95')
    secondary_color = models.CharField(max_length=100, default='#557A95')
    seo_title = models.CharField(max_length=200, null=True, blank=True)
    seo_description = models.TextField(null=True, blank=True)
    seo_keywords = models.TextField(help_text=_('Seperate with comma'), null=True, blank=True)
    banner_title = models.CharField(max_length=200, null=True, blank=True)
    banner_description = models.TextField(null=True, blank=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    data = JSONField(default=dict)

    def __str__(self):
        return self.client.domain_url

    def save(self, *args, **kwargs):
        color_fields = ['primary_color', 'secondary_color']
        for field in color_fields:
            if not getattr(self, field).startswith('#'):
                setattr(self, field, '#' + getattr(self, field))
        super(SiteSettings, self).save(*args, **kwargs)

    @property
    def primary_rgb(self):
        color = self.primary_color.replace('#', '')
        return ','.join(list(str(int(color[i:i + 2], 16)) for i in (0, 2, 4)))

    @property
    def secondary_rgb(self):
        color = self.secondary_color.replace('#', '')
        return ','.join(list(str(int(color[i:i + 2], 16)) for i in (0, 2, 4)))

    @property
    def alt_primary(self):
        clr = [str(int(int(unit)/2)) for unit in self.primary_rgb.split(',')]
        return ','.join(clr)

    @property
    def alt_secondary(self):
        clr = [str(int(int(unit) / 2)) for unit in self.secondary_rgb.split(',')]
        return ','.join(clr)


class SocialProfile(SoftDeletableModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    pinterest = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    stackoverflow = models.URLField(blank=True, null=True)
    behance = models.URLField(blank=True, null=True)
    dribbble = models.URLField(blank=True, null=True)
    medium = models.URLField(blank=True, null=True)
    quora = models.URLField(blank=True, null=True)
    vimeo = models.URLField(blank=True, null=True)
    reverbnation = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    tumblr = models.URLField(blank=True, null=True)
    reddit = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    foursquare = models.URLField(blank=True, null=True)
    vine = models.URLField(blank=True, null=True)
    personal_website = models.URLField(blank=True, null=True)


MONTHS = (
    ('01', _('January')),
    ('02', _('February')),
    ('03', _('March')),
    ('04', _('April')),
    ('05', _('May')),
    ('06', _('June')),
    ('07', _('July')),
    ('08', _('August')),
    ('09', _('September')),
    ('10', _('October')),
    ('11', _('November')),
    ('12', _('December')),
)


class EducationProfile(SoftDeletableModel):
    place = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    degree = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, null=True)
    from_month = models.CharField(max_length=10, choices=MONTHS, blank=True, null=True)
    from_year = models.CharField(max_length=4, default='2019')
    to_month = models.CharField(max_length=10, choices=MONTHS, blank=True, null=True)
    to_year = models.CharField(max_length=4, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.place + ',' + self.city

    @property
    def edit_url(self):
        return reverse('users:education-edit', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('users:education-delete', kwargs={'pk': self.id})


class CareerProfile(SoftDeletableModel):
    designation = models.CharField(max_length=100, default='')
    place = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=100, default='')
    description = models.TextField(blank=True, null=True)
    from_month = models.CharField(max_length=10, choices=MONTHS, null=True, blank=True)
    from_year = models.CharField(max_length=4, default='2019')
    to_month = models.CharField(max_length=10, choices=MONTHS, blank=True, null=True)
    to_year = models.CharField(max_length=4, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.designation + ', ' + self.place

    @property
    def edit_url(self):
        return reverse('users:careers-edit', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('users:careers-delete', kwargs={'pk': self.id})


class ExtraCurricularProfile(SoftDeletableModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='')
    description = models.TextField(null=True, blank=True)


def title_text_image_user_aware_upload_to(instance, filename):
    return os.path.join(instance.user.username, 'portfolio', 'works', filename)


class TitleTextImageModel(SoftDeletableModel, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='')
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=title_text_image_user_aware_upload_to)

    class Meta:
        abstract = True


def banner_media_user_aware_upload_to(instance, filename):
    return os.path.join(instance.user.username, 'banner-media', filename)


class BannerMedia(SoftDeletableModel, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.FileField(upload_to=banner_media_user_aware_upload_to, validators=[FileExtensionValidator(
        allowed_extensions=['mp4', 'mov', '3gp', 'png', 'jpg', 'gif'])])

    def __str__(self):
        return self.user.get_full_name()


class WorksProfile(TitleTextImageModel):
    link = models.URLField(default='', blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def edit_url(self):
        return reverse('users:works-edit', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('users:works-delete', kwargs={'pk': self.id})


class OfferProfile(TitleTextImageModel):
    def __str__(self):
        return self.title

    @property
    def edit_url(self):
        return reverse('users:offer-edit', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('users:offer-delete', kwargs={'pk': self.id})


class SkillProfile(SoftDeletableModel, TimeStampedModel):
    title = models.CharField(max_length=100, default='')
    skill_level = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.skill_level) + '% proficiency level,' + self.title

    @property
    def level(self):
        sk_lv = self.skill_level
        if sk_lv >= 85:
            return 'Veteran'
        elif 70 < sk_lv < 85:
            return 'Senior'
        elif 60 < sk_lv < 70:
            return 'Mid-Level'
        elif 50 < sk_lv < 60:
            return 'Junior'
        return 'Beginner'

    @property
    def edit_url(self):
        return reverse('users:skills-edit', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('users:skills-delete', kwargs={'pk': self.id})


class CustomProfile(SoftDeletableModel, TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=200)
    sub_header = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return f'{self.header} - {self.sub_header}'

    @property
    def edit_url(self):
        return reverse('users:others-edit', kwargs={'pk': self.id})

    @property
    def delete_url(self):
        return reverse('users:others-delete', kwargs={'pk': self.id})