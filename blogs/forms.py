from django import forms
from django.utils.translation import ugettext_lazy as _

from blogs.models import BlogPost, BlogCategory, Comment
from wresume.utils import CustomClearableFileInput


class BlogPostForm(forms.ModelForm):
    def __init__(self, **kwargs):
        site = kwargs.pop('site', None)
        super(BlogPostForm, self).__init__(**kwargs)
        self.fields['category'].queryset = BlogCategory.objects.filter(site=site)

    class Meta:
        model = BlogPost
        fields = (
            'title',
            'is_featured',
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
            'seo_desc': _('SEO Description'),
            'is_featured': _('Show in Featured Section')
        }
        help_texts = {
            'is_featured': 'This can only take maximum of four active posts at a time, you might '
                           'need to unmark old posts to accommodate new ones in the list.'
        }
        widgets = {
            'author': forms.HiddenInput,
            'seo_desc': forms.Textarea(attrs={'rows': 2}),
            'site': forms.HiddenInput,
            'image': CustomClearableFileInput
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


class BlogCommentForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    parent_id = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Comment
        fields = (
            'name',
            'email',
            'post',
            'content',
            'parent_id'
        )
        widgets = {
            'post': forms.HiddenInput,
        }
