from copy import copy, deepcopy

from allauth.account.forms import SignupForm
from django import forms

from users.models import User, Profile, SiteSettings, SocialProfile, EducationProfile, CareerProfile, SkillProfile, \
    WorksProfile, OfferProfile, BannerMedia


class SignUpForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop('autofocus', None)
        self.fields['email'].widget.attrs.update({'autofocus': 'autofocus'})

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'email',
            'password'
        )

    def signup(self, request, user):
        pass


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'photo'
        )


class SettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            'favicon',
            'logo',
            'banner_title',
            'banner_description',
            'seo_title',
            'seo_description',
            'seo_keywords',
        )
        widgets = {
            'banner_description': forms.Textarea(attrs={'rows': 3}),
            'seo_description': forms.Textarea(attrs={'rows': 3}),
            'seo_keywords': forms.Textarea(attrs={'rows': 3}),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'city',
            'date_of_birth',
            'phone',
            'bio'
        )
        widgets = {
            'date_of_birth': forms.TextInput(attrs={'class': 'wresume-datepicker'}),
            'bio': forms.Textarea(attrs={'rows': 4})
        }


class SocialForm(forms.ModelForm):
    class Meta:
        model = SocialProfile
        exclude = (
            'is_removed',
        )
        widgets = {
            'user': forms.HiddenInput
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = EducationProfile
        fields = (
            'user',
            'place',
            'city',
            'country',
            'degree',
            'description',
            'from_month',
            'from_year',
            'to_month',
            'to_year'
        )
        widgets = {
            'user': forms.HiddenInput,
            'description': forms.Textarea(attrs={'rows': '3'})
        }


class CareerForm(forms.ModelForm):
    class Meta:
        model = CareerProfile
        fields = (
            'designation',
            'place',
            'city',
            'country',
            'description',
            'from_month',
            'from_year',
            'to_month',
            'to_year',
            'user'
        )
        widgets = {
            'user': forms.HiddenInput,
            'description': forms.Textarea(attrs={'rows': '3'})
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = SkillProfile
        fields = (
            'title',
            'skill_level',
            'description',
            'user'
        )
        widgets = {
            'user': forms.HiddenInput,
            'description': forms.Textarea(attrs={'rows': '3'})
        }


class WorksForm(forms.ModelForm):
    class Meta:
        model = WorksProfile
        fields = (
            'user',
            'title',
            'description',
            'image'
        )
        widgets = {
            'user': forms.HiddenInput,
            'description': forms.Textarea(attrs={'rows': '3'})
        }


class OfferForm(forms.ModelForm):
    class Meta:
        model = OfferProfile
        fields = (
            'user',
            'title',
            'description',
            'image'
        )
        widgets = {
            'user': forms.HiddenInput,
            'description': forms.Textarea(attrs={'rows': '3'})
        }


class BannerMediaForm(forms.ModelForm):
    class Meta:
        model = BannerMedia
        fields = (
            'user',
            'media'
        )
        widgets = {
            'user': forms.HiddenInput,
        }
