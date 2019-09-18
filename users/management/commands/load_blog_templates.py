from django.core.management import BaseCommand
from django.templatetags.static import static

from blogs.models import Template

BLOG_TEMPLATES = [
    # {
    #     'name': 'Callie',
    #     'template_folder': 'blog-templates/callie/',
    #     'screenshot': static('blog-assets/callie/img/screenshot.png')
    # },
    {
        'name': 'Eden',
        'template_folder': 'blog-templates/eden/',
        'screenshot': static('blog-assets/eden/img/screenshot.png')
    }
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for temp in BLOG_TEMPLATES:
            Template.objects.get_or_create(**temp)
