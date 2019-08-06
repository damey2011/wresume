from django.urls import path

from home import views

app_name = 'home'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='public_home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('change-site/', views.DashboardView.as_view(), name='change-site'),
]
