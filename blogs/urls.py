from django.urls import path

from blogs import views

app_name = 'blogs'

urlpatterns = [
    path('<str:slug>/', views.BlogPostView.as_view(), name='blog-post')
]
