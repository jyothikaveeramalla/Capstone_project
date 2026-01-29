from django.urls import path
from . import views

urlpatterns = [
    path('', views.collaborations_list_view, name='collaborations_list'),
    path('request/new/', views.new_collaboration_request_view, name='new_collab_request'),
    path('request/<int:request_id>/', views.collaboration_request_detail_view, name='collab_request_detail'),
    path('request/<int:request_id>/accept/', views.accept_collaboration_view, name='accept_collab'),
    path('request/<int:request_id>/reject/', views.reject_collaboration_view, name='reject_collab'),
    path('<int:collab_id>/', views.active_collaboration_detail_view, name='collab_detail'),
    path('<int:collab_id>/posts/', views.collaboration_posts_view, name='collab_posts'),
    path('<int:collab_id>/post/add/', views.add_collaboration_post_view, name='add_collab_post'),
]
