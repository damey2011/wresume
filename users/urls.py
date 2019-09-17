from django.urls import path, reverse_lazy
from django.utils.translation import ugettext_lazy as _

from users import views
from users.forms import EducationForm, CareerForm, SkillForm, WorksForm, OfferForm, BannerMediaForm, CustomProfileForm
from users.models import EducationProfile, CareerProfile, SkillProfile, WorksProfile, OfferProfile, BannerMedia, \
    CustomProfile

app_name = 'users'

urlpatterns = [
    path('', views.BasicProfileView.as_view(), name='basic_profile'),
    path('resume/', views.ResumeFormView.as_view(), name='resume'),
    path('social/', views.SocialFormView.as_view(), name='social'),
    path('settings/', views.SettingsView.as_view(), name='settings'),


    path('education/', views.MultiEntryView.as_view(
        extra_context={'education_tab': True, 'basic_tab': True},
        form_class=EducationForm,
        success_url=reverse_lazy('users:education'),
        add_item_title=_('Add Education'),
        inject_initial=['user'],
        model=EducationProfile,
        object_list_filter=['user']
    ), name='education'),
    path('education/<int:pk>/update/', views.MultiEntryUpdateView.as_view(
        extra_context={'education_tab': True, 'basic_tab': True},
        form_class=EducationForm,
        success_url=reverse_lazy('users:education'),
        model=EducationProfile,
    ), name='education-edit'),
    path('education/<int:pk>/delete/', views.MultiEntryDeleteView.as_view(
        extra_context={'education_tab': True, 'basic_tab': True},
        success_url=reverse_lazy('users:education'),
        model=EducationProfile,
    ), name='education-delete'),


    path('careers/', views.MultiEntryView.as_view(
        extra_context={'careers_tab': True, 'basic_tab': True},
        form_class=CareerForm,
        form_title=_('Add Work Experience'),
        add_item_title=_('Add Experience'),
        success_url=reverse_lazy('users:careers'),
        inject_initial=['user'],
        model=CareerProfile,
        object_list_filter=['user']
    ), name='careers'),
    path('careers/<int:pk>/update/', views.MultiEntryUpdateView.as_view(
        extra_context={'careers_tab': True, 'basic_tab': True},
        form_class=CareerForm,
        success_url=reverse_lazy('users:careers'),
        model=CareerProfile,
    ), name='careers-edit'),
    path('careers/<int:pk>/delete/', views.MultiEntryDeleteView.as_view(
        extra_context={'careers_tab': True, 'basic_tab': True},
        success_url=reverse_lazy('users:careers'),
        model=CareerProfile,
    ), name='careers-delete'),


    path('skills/', views.MultiEntryView.as_view(
        extra_context={'skills_tab': True, 'basic_tab': True},
        form_class=SkillForm,
        form_title=_('Add Skill'),
        add_item_title=_('Add Skill'),
        success_url=reverse_lazy('users:skills'),
        inject_initial=['user'],
        model=SkillProfile,
        object_list_filter=['user']
    ), name='skills'),
    path('skills/<int:pk>/update/', views.MultiEntryUpdateView.as_view(
        extra_context={'skills_tab': True, 'basic_tab': True},
        form_class=SkillForm,
        success_url=reverse_lazy('users:skills'),
        model=SkillProfile,
    ), name='skills-edit'),
    path('skills/<int:pk>/delete/', views.MultiEntryDeleteView.as_view(
        extra_context={'skills_tab': True, 'basic_tab': True},
        success_url=reverse_lazy('users:skills'),
        model=SkillProfile,
    ), name='skills-delete'),


    path('works/', views.MultiEntryView.as_view(
        extra_context={'works_tab': True, 'advanced_tab': True},
        form_class=WorksForm,
        form_title=_('Add a personal project or work done'),
        add_item_title=_('Add Work/Project'),
        success_url=reverse_lazy('users:works'),
        inject_initial=['user'],
        model=WorksProfile,
        object_list_filter=['user']
    ), name='works'),
    path('works/<int:pk>/update/', views.MultiEntryUpdateView.as_view(
        extra_context={'works_tab': True, 'advanced_tab': True},
        form_class=WorksForm,
        success_url=reverse_lazy('users:works'),
        model=WorksProfile,
    ), name='works-edit'),
    path('works/<int:pk>/delete/', views.MultiEntryDeleteView.as_view(
        extra_context={'works_tab': True, 'advanced_tab': True},
        success_url=reverse_lazy('users:works'),
        model=WorksProfile,
    ), name='works-delete'),


    path('offer/', views.MultiEntryView.as_view(
        extra_context={'offer_tab': True, 'advanced_tab': True},
        form_class=OfferForm,
        form_title=_('What do you offer your client'),
        add_item_title=_('Add Offer'),
        success_url=reverse_lazy('users:offer'),
        inject_initial=['user'],
        model=OfferProfile,
        object_list_filter=['user']
    ), name='offer'),
    path('offer/<int:pk>/update/', views.MultiEntryUpdateView.as_view(
        extra_context={'offer_tab': True, 'advanced_tab': True},
        form_class=OfferForm,
        success_url=reverse_lazy('users:offer'),
        model=OfferProfile,
    ), name='offer-edit'),
    path('offer/<int:pk>/delete/', views.MultiEntryDeleteView.as_view(
        extra_context={'offer_tab': True, 'advanced_tab': True},
        success_url=reverse_lazy('users:offer'),
        model=OfferProfile,
    ), name='offer-delete'),


    path('banner/', views.MultiEntryView.as_view(
        extra_context={'banner_tab': True, 'basic_tab': True},
        form_class=BannerMediaForm,
        form_title=_('Add banners you would want to use on your page (slide is applied when more than one is used)'),
        add_item_title=_('Add Banner Image'),
        success_url=reverse_lazy('users:banner'),
        inject_initial=['user'],
        model=BannerMedia,
        object_list_filter=['user']
    ), name='banner'),
    path('banner/<int:pk>/update/', views.MultiEntryUpdateView.as_view(
        extra_context={'banner_tab': True, 'basic_tab': True},
        form_class=BannerMediaForm,
        success_url=reverse_lazy('users:offer'),
        model=BannerMedia,
    ), name='banner-edit'),
    path('banner/<int:pk>/delete/', views.MultiEntryDeleteView.as_view(
        extra_context={'banner_tab': True, 'basic_tab': True},
        success_url=reverse_lazy('users:offer'),
        model=BannerMedia,
    ), name='banner-delete'),

    path('others/', views.MultiEntryView.as_view(
        extra_context={'others_tab': True, 'basic_tab': True},
        form_title=_('Add other section (e.g. Volunteers, Certifications..)'),
        form_class=CustomProfileForm,
        success_url=reverse_lazy('users:others'),
        add_item_title=_('Add Section'),
        inject_initial=['user'],
        model=CustomProfile,
        object_list_filter=['user']
    ), name='others'),
    path('others/<int:pk>/update/', views.MultiEntryUpdateView.as_view(
        extra_context={'others_tab': True, 'basic_tab': True},
        form_class=CustomProfileForm,
        success_url=reverse_lazy('users:others'),
        model=CustomProfile,
    ), name='others-edit'),
    path('others/<int:pk>/delete/', views.MultiEntryDeleteView.as_view(
        extra_context={'others_tab': True, 'basic_tab': True},
        success_url=reverse_lazy('users:education'),
        model=CustomProfile,
    ), name='others-delete'),
]
