from django import forms

from documents.models import Document
from wresume.utils import CustomClearableFileInput


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = (
            'title',
            'description',
            'doc',
            'user'
        )
        widgets = {
            'user': forms.HiddenInput,
            'doc': CustomClearableFileInput
        }