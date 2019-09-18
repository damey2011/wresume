from django.urls import path

from blogs import views

app_name = 'blogs'

urlpatterns = [
    path('', views.BlogPostListView.as_view(), name='blog-post-list'),
    path('test/', views.BlogTestView.as_view(), name='test'),
    path('categories/', views.BlogCategoriesView.as_view(), name='categories'),
    path('archive/', views.BlogArchivesView.as_view(), name='archives'),
    path('contact/', views.BlogContactView.as_view(), name='contact'),
    path('categories/<int:pk>/', views.BlogCategoryView.as_view(), name='category-detail'),
    path('<slug:slug>/', views.BlogPostView.as_view(), name='blog-post')
]
