from django import template
from django.forms import Textarea
from django.urls import reverse

from resumes.models import SiteTemplate

register = template.Library()


@register.simple_tag(takes_context=True)
def user_sites(context):
    request = context['request']
    return request.user.client_set.all()


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
