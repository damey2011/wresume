from django.contrib import admin

# Register your models here.
from resumes.models import Template, SiteTemplate, TemplateAsset, ContactFormData, DBDumps

admin.site.register(Template)
admin.site.register(SiteTemplate)
admin.site.register(TemplateAsset)
admin.site.register(ContactFormData)
admin.site.register(DBDumps)