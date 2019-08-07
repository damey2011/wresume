from django.urls import path

from home import views_public

app_name = 'home'

urlpatterns = [
    path('', views_public.HomePageView.as_view(), name='public_home'),
    path('dashboard/', views_public.DashboardView.as_view(), name='dashboard'),
    path('change-site/', views_public.DashboardView.as_view(), name='change-site'),
]
