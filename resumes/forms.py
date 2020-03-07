from django import forms

from resumes.models import Template


class CreateTemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = (
            'name',
            'content',
            'full_content',
            'styles',
            'fonts',
            'js',
            'gjs_components',
            'owner'
        )
        widgets = {
            'owner': forms.HiddenInput,
            'content': forms.HiddenInput,
            'full_content': forms.HiddenInput,
            'is_public': forms.HiddenInput,
            'styles': forms.HiddenInput,
            'fonts': forms.HiddenInput,
            'js': forms.HiddenInput,
            'gjs_components': forms.HiddenInput
        }
