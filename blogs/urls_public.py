from django.urls import path
from blogs import views_public as views

app_name = 'blogs_public'

urlpatterns = [
    path('', views.BlogPostsView.as_view(), name='list'),
    path('categories/', views.BlogCategoriesView.as_view(), name='categories'),
    path('categories/<int:pk>/delete/', views.BlogCategoryDeleteView.as_view(), name='delete-category'),
    path('categories/create/', views.CreateCategoryView.as_view(), name='create-categories'),
    path('write/', views.WritePostView.as_view(), name='write'),
    path('templates/', views.BlogTemplatesView.as_view(), name='template-list'),
    path('templates/<int:pk>/activate/', views.ActivateBlogTemplateView.as_view(), name='template-activate'),
    path('templates/<int:pk>/deactivate/', views.DeActivateBlogTemplateView.as_view(), name='template-deactivate'),
    path('post/<int:pk>/edit/', views.EditPostView.as_view(), name='edit'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete'),
]
