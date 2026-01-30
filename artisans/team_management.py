"""
Team Management Views

This module handles team creation, member management, and team operations.
Only authenticated artisans can create and manage teams.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import get_user_model
from accounts.decorators import artisan_required
from artisans.models import ArtisanProfile, ArtisanTeam, ArtisanTeamMember

User = get_user_model()


@login_required
@artisan_required
@require_http_methods(["GET", "POST"])
def create_team_view(request):
    """
    Create a new artisan team.
    
    GET: Display the team creation form
    POST: Save the new team
    
    Access: Only authenticated artisans can create teams
    """
    if request.method == 'POST':
        team_name = request.POST.get('name', '').strip()
        team_description = request.POST.get('description', '').strip()
        
        if not team_name:
            messages.error(request, 'Team name is required.')
            return redirect('create_team')
        
        try:
            with transaction.atomic():
                # Create the team
                team = ArtisanTeam.objects.create(
                    name=team_name,
                    description=team_description,
                    owner=request.user
                )
                
                # Add the creator as admin
                artisan = ArtisanProfile.objects.get(user=request.user)
                artisan.team = team
                artisan.save()
                
                ArtisanTeamMember.objects.create(
                    team=team,
                    user=request.user,
                    role='admin'
                )
                
                messages.success(request, f'Team "{team_name}" has been created successfully!')
                return redirect('team_dashboard', team_id=team.id)
        except ArtisanProfile.DoesNotExist:
            messages.error(request, 'You must have an artisan profile to create a team.')
            return redirect('artisan_setup')
        except Exception as e:
            messages.error(request, f'Error creating team: {str(e)}')
    
    context = {
        'page_title': 'Create a New Team',
    }
    
    return render(request, 'teams/create_team.html', context)


@login_required
@artisan_required
@require_http_methods(["GET"])
def team_dashboard_view(request, team_id):
    """
    View team dashboard with members and products.
    
    Access: Only team members can view the team dashboard
    """
    team = get_object_or_404(ArtisanTeam, id=team_id)
    
    # Check if user is a team member
    if not team.has_member(request.user):
        messages.error(request, 'You do not have access to this team.')
        return redirect('dashboard')
    
    members = team.get_members()
    products = team.products.filter(status='active').order_by('-created_at')
    
    context = {
        'team': team,
        'members': members,
        'products': products,
        'page_title': f'{team.name} Dashboard',
        'is_admin': team.owner == request.user or team.members.filter(user=request.user, role='admin').exists(),
    }
    
    return render(request, 'teams/team_dashboard.html', context)


@login_required
@artisan_required
@require_http_methods(["GET", "POST"])
def add_team_member_view(request, team_id):
    """
    Add a new member to the team.
    
    GET: Display the add member form
    POST: Add the member to the team
    
    Access: Only team admins can add members
    """
    team = get_object_or_404(ArtisanTeam, id=team_id)
    
    # Check if user is team admin
    is_admin = team.owner == request.user or team.members.filter(user=request.user, role='admin').exists()
    if not is_admin:
        messages.error(request, 'You do not have permission to add members to this team.')
        return redirect('team_dashboard', team_id=team.id)
    
    if request.method == 'POST':
        member_email = request.POST.get('member_email', '').strip()
        member_role = request.POST.get('role', 'member')
        
        if not member_email:
            messages.error(request, 'Email address is required.')
            return redirect('add_team_member', team_id=team.id)
        
        try:
            # Find user by email
            user = User.objects.get(email=member_email)
            
            # Check if user has an artisan profile
            artisan = ArtisanProfile.objects.get(user=user)
            
            # Check if user is already a member
            if team.has_member(user):
                messages.error(request, f'{user.get_full_name()} is already a member of this team.')
                return redirect('add_team_member', team_id=team.id)
            
            # Add user to team
            team.add_member(user, role=member_role)
            
            # Update artisan's team reference
            artisan.team = team
            artisan.save()
            
            messages.success(request, f'{user.get_full_name()} has been added to the team.')
            return redirect('team_dashboard', team_id=team.id)
        
        except User.DoesNotExist:
            messages.error(request, f'User with email "{member_email}" not found.')
        except ArtisanProfile.DoesNotExist:
            messages.error(request, f'User with email "{member_email}" does not have an artisan profile.')
        except Exception as e:
            messages.error(request, f'Error adding member: {str(e)}')
    
    context = {
        'team': team,
        'page_title': f'Add Member to {team.name}',
    }
    
    return render(request, 'teams/add_team_member.html', context)


@login_required
@artisan_required
@require_http_methods(["POST"])
def remove_team_member_view(request, team_id, member_id):
    """
    Remove a member from the team.
    
    Access: Only team admins can remove members
    """
    team = get_object_or_404(ArtisanTeam, id=team_id)
    
    # Check if user is team admin
    is_admin = team.owner == request.user or team.members.filter(user=request.user, role='admin').exists()
    if not is_admin:
        messages.error(request, 'You do not have permission to remove members from this team.')
        return redirect('team_dashboard', team_id=team.id)
    
    # Prevent removing the team owner
    member = get_object_or_404(User, id=member_id)
    if member == team.owner:
        messages.error(request, 'You cannot remove the team owner.')
        return redirect('team_dashboard', team_id=team.id)
    
    try:
        with transaction.atomic():
            # Remove from team members
            team.remove_member(member)
            
            # Update artisan's team reference
            artisan = ArtisanProfile.objects.get(user=member)
            artisan.team = None
            artisan.save()
            
            messages.success(request, f'{member.get_full_name()} has been removed from the team.')
    except ArtisanProfile.DoesNotExist:
        messages.error(request, 'Error removing member.')
    except Exception as e:
        messages.error(request, f'Error removing member: {str(e)}')
    
    return redirect('team_dashboard', team_id=team.id)


@login_required
@artisan_required
@require_http_methods(["POST"])
def leave_team_view(request, team_id):
    """
    Leave a team.
    
    Access: Any team member can leave (except the owner cannot leave without reassigning ownership)
    """
    team = get_object_or_404(ArtisanTeam, id=team_id)
    
    # Check if user is the owner
    if team.owner == request.user:
        messages.error(request, 'You cannot leave a team you own. Please reassign ownership first.')
        return redirect('team_dashboard', team_id=team.id)
    
    try:
        with transaction.atomic():
            # Remove from team
            team.remove_member(request.user)
            
            # Update artisan's team reference
            artisan = ArtisanProfile.objects.get(user=request.user)
            artisan.team = None
            artisan.save()
            
            messages.success(request, f'You have left the team "{team.name}".')
            return redirect('dashboard')
    except ArtisanProfile.DoesNotExist:
        messages.error(request, 'Error leaving team.')
        return redirect('team_dashboard', team_id=team.id)
    except Exception as e:
        messages.error(request, f'Error leaving team: {str(e)}')
        return redirect('team_dashboard', team_id=team.id)


@login_required
@artisan_required
@require_http_methods(["GET"])
def my_teams_view(request):
    """
    View all teams the current user is a member of.
    
    Access: Only authenticated artisans
    """
    # Get teams where user is a member
    user_teams = ArtisanTeam.objects.filter(members__user=request.user).distinct()
    
    context = {
        'teams': user_teams,
        'page_title': 'My Teams',
    }
    
    return render(request, 'teams/my_teams.html', context)
