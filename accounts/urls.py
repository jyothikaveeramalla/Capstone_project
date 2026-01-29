from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('signin/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('artisan/setup/', views.artisan_profile_setup, name='artisan_setup'),
    path('influencer/setup/', views.influencer_profile_setup, name='influencer_setup'),
]
