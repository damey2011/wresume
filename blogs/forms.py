from django import forms
from django.utils.translation import ugettext_lazy as _

from blogs.models import BlogPost, BlogCategory, Comment


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
