from allauth.account.forms import SignupForm
from django import forms

from resumes.models import ContactFormData
from users.models import User, Profile, SiteSettings, SocialProfile, EducationProfile, CareerProfile, SkillProfile, \
    WorksProfile, OfferProfile, BannerMedia, CustomProfile


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
    def __init__(self, **kwargs):
        super(UserForm, self).__init__(**kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'title',
            'photo'
        )
        labels = {
            'title': 'Job Title (e.g. Software Developer)'
        }
        help_texts = {
            'username': None
        }


class SettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            'favicon',
            'logo',
            # 'banner_title',
            # 'banner_description',
            'seo_title',
            'seo_description',
            'seo_keywords',
        )
        widgets = {
            'banner_description': forms.Textarea(attrs={'rows': 3}),
            'seo_description': forms.Textarea(attrs={'rows': 3}),
            'seo_keywords': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'seo_title': 'SEO Title',
            'seo_description': 'SEO Description',
            'seo_keywords': 'SEO Keywords'
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
        labels = {
            'bio': 'Bio/Summary'
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
        labels = {
            'place': 'Institution'
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
        labels = {
            'place': 'Company/Organization',
            'to_year': 'To year',
            'to_month': 'To month'
        }
        help_texts = {
            'designation': 'Your position in the company',
            'description': 'Your job description and roles in the company',
            'to_year': 'Leave blank for present',
            'to_month': 'Leave blank for present'
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
        labels = {
            'title': 'Skill Name'
        }
        help_texts = {
            'title': 'e.g. Sewing, Coding, Python, Excel etc',
            'skill_level': 'Rate this skill from 0-100',
            'description': 'You can include certifications and degrees associated with this skills'
        }


class WorksForm(forms.ModelForm):
    class Meta:
        model = WorksProfile
        fields = (
            'user',
            'title',
            'description',
            'link',
            'image'
        )
        widgets = {
            'user': forms.HiddenInput,
            'description': forms.Textarea(attrs={'rows': '3'})
        }
        labels = {
            'title': 'Work/Project Name'
        }
        help_texts = {
            'link': 'A URL to showcase the work (if applicable)',
            'image': 'An image we can display on the site for the works section',
            'description': 'Tell us what this work entailed and the kind of project'
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


class ContactDataForm(forms.ModelForm):
    class Meta:
        model = ContactFormData
        fields = (
            'name',
            'email',
            'subject',
            'message',
            'client'
        )
        widgets = {
            'client': forms.HiddenInput,
            'message': forms.Textarea(attrs={'rows': 3})
        }


class CustomProfileForm(forms.ModelForm):
    class Meta:
        model = CustomProfile
        fields = (
            'header',
            'sub_header',
            'content',
            'user'
        )
        widgets = {
            'user': forms.HiddenInput
        }