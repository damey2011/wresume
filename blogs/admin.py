from django.contrib import admin

from blogs.models import BlogPost, Comment, BlogImage, BlogCategory


admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(BlogImage)
admin.site.register(BlogCategory)
