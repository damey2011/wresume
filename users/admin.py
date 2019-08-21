from django.contrib import admin

from users.models import User, Profile, Client, SiteSettings, SocialProfile, EducationProfile, CareerProfile, \
    ExtraCurricularProfile, BannerMedia, WorksProfile, OfferProfile, SkillProfile

admin.site.register(User)
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
