from django.urls import path
from blogs import views_public as views

app_name = 'blogs_public'

urlpatterns = [
    path('', views.BlogPostsView.as_view(), name='list'),
    path('categories/', views.BlogCategoriesView.as_view(), name='categories'),
    path('categories/<int:pk>/delete/', views.BlogCategoryDeleteView.as_view(), name='delete-category'),
    path('categories/create/', views.CreateCategoryView.as_view(), name='create-categories'),
    path('write/', views.WritePostView.as_view(), name='write'),
]
