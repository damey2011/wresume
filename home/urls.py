from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
    path('', views.TenantHomeView.as_view(), name='tenant_home'),
    path('<slug:slug>/', views.TenantHomeView.as_view(), name='tenant_page'),
    path('test/', views.test, name='tenant_home_test'),
]
