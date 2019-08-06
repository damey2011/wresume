from django import forms
from django.utils.translation import ugettext_lazy as _

from blogs.models import BlogPost, BlogCategory


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = (
            'title',
            'content',
            'image',
            'category',
            'seo_desc',
            'seo_keywords',
            'author',
            'site'
        )
        labels = {
            'seo_keywords': _('SEO keywords (seperate with commas)'),
            'seo_desc': _('SEO Description')
        }
        widgets = {
            'author': forms.HiddenInput,
            'seo_desc': forms.Textarea(attrs={'rows': 2}),
            'site': forms.HiddenInput
        }


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = (
            'category',
            'site'
        )
        widgets = {
            'site': forms.HiddenInput
        }
