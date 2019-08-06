from django.urls import path

from resumes import views

app_name = 'resumes'

urlpatterns = [
    path('', views.ListTemplatesView.as_view(), name='list'),
    path('my-templates/', views.ListMyTemplatesView.as_view(), name='my-templates'),
    path('my-templates/<int:pk>/', views.PreviewMyTemplateView.as_view(), name='my-template-preview'),
    path('my-templates/<int:pk>/activate/', views.MyTemplateActivateView.as_view(), name='my-template-activate'),
    path('my-templates/<int:pk>/update/', views.UpdateMyTemplateView.as_view(), name='my-template-update'),
    path('my-templates/<int:pk>/deactivate/', views.MyTemplateDeactivateView.as_view(), name='my-template-deactivate'),
    path('my-templates/<int:pk>/delete/', views.MyTemplateDeleteView.as_view(), name='my-template-delete'),
    path('create/', views.CreateTemplateView.as_view(), name='create-template'),
    path('gjs/upload/<int:user>/', views.GJSUploadView.as_view(), name='gjs-uploads'),
]
