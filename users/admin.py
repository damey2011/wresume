from django.contrib import admin
from django.contrib.admin import ModelAdmin

from users.models import User, Profile, Client, SiteSettings, SocialProfile, EducationProfile, CareerProfile, \
    ExtraCurricularProfile, BannerMedia, WorksProfile, OfferProfile, SkillProfile


class UserAdmin(ModelAdmin):
    change_form_template = 'loginas/change_form.html'


admin.site.register(User, UserAdmin)
admin.site.register(Client)
admin.site.register(Profile)
admin.site.register(SiteSettings)
admin.site.register(SocialProfile)
admin.site.register(EducationProfile)
admin.site.register(CareerProfile)
admin.site.register(ExtraCurricularProfile)
admin.site.register(BannerMedia)
admin.site.register(WorksProfile)
admin.site.register(OfferProfile)
admin.site.register(SkillProfile)
