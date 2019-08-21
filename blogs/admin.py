from django.contrib import admin

# Register your models here.
from blogs.models import BlogPost, Comment, BlogImage, BlogCategory

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(BlogImage)
admin.site.register(BlogCategory)