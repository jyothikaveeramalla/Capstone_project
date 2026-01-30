from django.urls import path
from . import views
from .team_management import (
    create_team_view, team_dashboard_view, add_team_member_view, 
    remove_team_member_view, leave_team_view, my_teams_view
)

urlpatterns = [
    # Artisan list and detail views
    path('', views.artisans_list_view, name='artisans_list'),
    path('<int:artisan_id>/', views.artisan_detail_view, name='artisan_detail'),
    path('<int:artisan_id>/products/', views.artisan_products_view, name='artisan_products'),
    
    # Team management
    path('teams/my/', my_teams_view, name='my_teams'),
    path('teams/create/', create_team_view, name='create_team'),
    path('teams/<int:team_id>/', team_dashboard_view, name='team_dashboard'),
    path('teams/<int:team_id>/add-member/', add_team_member_view, name='add_team_member'),
    path('teams/<int:team_id>/remove-member/<int:member_id>/', remove_team_member_view, name='remove_team_member'),
    path('teams/<int:team_id>/leave/', leave_team_view, name='leave_team'),
]
