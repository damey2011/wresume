from django import template
from django.conf import settings
from django.forms import Textarea
from django.templatetags.static import static
from django.urls import reverse

from resumes.models import SiteTemplate
from wresume.utils import get_tenant_url, get_tenant

register = template.Library()


@register.simple_tag(takes_context=True)
def user_sites(context):
    request = context['request']
    return request.user.client_set.all()


@register.simple_tag(takes_context=True)
def current_domain_site(context):
    request = context.get('request')
    return request.scheme + '://' + request.META.get('HTTP_HOST')


@register.simple_tag(takes_context=True)
def selected_site(context):
    request = context['request']
    return request.session.get('site_id', user_sites(context).first().id)


@register.simple_tag(takes_context=True)
def upload_url(context):
    request = context['request']
    return request.build_absolute_uri(reverse('resumes:gjs-uploads', kwargs={'user': request.user.id}))


@register.simple_tag(takes_context=True)
def is_active_for_current_site(context, template_id):
    request = context['request']
    site_id = request.session.get('site_id')
    return SiteTemplate.objects.filter(template_id=template_id, site_id=site_id).exists()


@register.simple_tag
def is_text_area(field):
    return isinstance(field.field.widget, Textarea)


@register.simple_tag
def get_attr(obj, attr):
    if hasattr(obj, 'get_' + attr + '_display'):
        return getattr(obj, 'get_' + attr + '_display', '')()
    return getattr(obj, attr, '')


@register.filter
def image_or_not(image_field):
    if image_field:
        return image_field.url
    return static('images/new-images/noimage.png')


@register.simple_tag(takes_context=True)
def tenant(context):
    request = context.get('request')
    return request.tenant


@register.simple_tag
def t_user(tenant_):
    return tenant_.user


@register.simple_tag
def offer_icon(index):
    icons = [
        'icon-bulb',
        'icon-data',
        'icon-phone3',
        'icon-layers2',
    ]
    return icons[index % len(icons)]


@register.simple_tag
def color_index(index):
    if index < 8:
        return index
    return index % 7


@register.simple_tag
def index_is_odd(index):
    return index % 2 != 0


@register.simple_tag
def static_url():
    return settings.STATIC_URL


@register.simple_tag(takes_context=True)
def tenant_home_from_user(context):
    request = context.get('request')
    return get_tenant_url(get_tenant(request.user))
