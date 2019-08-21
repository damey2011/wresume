from django.urls import path

from blogs import views

app_name = 'blogs'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='blog-post-list'),
    path('<str:slug>/', views.BlogPostView.as_view(), name='blog-post')
]
