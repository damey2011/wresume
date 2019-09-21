import mimetypes
from html import escape

from django import template
from django.conf import settings
from django.forms import Textarea
from django.templatetags.static import static
from django.urls import reverse

from blogs.models import SiteBlogTemplate
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
def is_active_for_current_site(context, template_id, is_blog=False):
    request = context['request']
    site_id = request.session.get('site_id')
    if not is_blog:
        return SiteTemplate.objects.filter(template_id=template_id, site_id=site_id).exists()
    return SiteBlogTemplate.objects.filter(template_id=template_id, client_id=site_id).exists()


@register.simple_tag
def is_text_area(field):
    return isinstance(field.field.widget, Textarea)


@register.simple_tag
def get_attr(obj, attr):
    if hasattr(obj, 'get_' + attr + '_display'):
        attr = getattr(obj, 'get_' + attr + '_display', '')()
        return attr if attr else ''
    val = getattr(obj, attr, '')
    if not val:
        return ''
    if hasattr(val, 'url'):
        return '<a href="{}" target="_blank">View</a>'.format(val.url)
    return val


@register.filter
def image_or_not(image_field, default=static('images/new-images/noimage.png')):
    if image_field:
        return image_field.url
    return default


@register.filter
def image_or_def(image_field):
    if image_field:
        return image_field.url
    return static('images/default-banner.jpg')


@register.filter
def image_or_noperson(image_field):
    if image_field:
        return image_field.url
    return static('images/new-images/noperson.jpg')


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


@register.filter
def social_username(link):
    return link.split('/')[-1] if link else ''


@register.filter
def escape_html(content):
    return escape(content)


@register.simple_tag
def is_file_image(file):
    return 'image' in mimetypes.guess_type(file.path)[0]
