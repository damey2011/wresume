from django.urls import path

from documents import views

app_name = 'docs'

urlpatterns = [
    path('<slug:slug>/', views.DocumentPublicView.as_view(), name='shareable-view')
]