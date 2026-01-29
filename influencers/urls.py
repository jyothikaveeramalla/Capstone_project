from django.urls import path
from . import views

app_name = 'influencers'

urlpatterns = [
    path('', views.influencers_list_view, name='list'),
    path('<int:influencer_id>/', views.influencer_detail_view, name='detail'),
]
