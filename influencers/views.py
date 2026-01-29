from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import InfluencerProfile
from accounts.decorators import influencer_required, login_required
from collaborations.models import CollaborationRequest
from artisans.models import ArtisanProfile


@require_http_methods(["GET"])
def influencers_list_view(request):
    """
    List all influencers with search and filter
    """
    influencers = InfluencerProfile.objects.all()
    
    # Search by niche or name
    search = request.GET.get('search', '')
    if search:
        influencers = influencers.filter(
            Q(niche__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(bio__icontains=search)
        )
    
    # Filter by verified
    verified_only = request.GET.get('verified', False)
    if verified_only:
        influencers = influencers.filter(is_verified=True)
    
    # Filter by featured
    featured_only = request.GET.get('featured', False)
    if featured_only:
        influencers = influencers.filter(is_featured=True)
    
    # Sort options
    sort = request.GET.get('sort', '-rating')
    influencers = influencers.order_by(sort)
    
    context = {
        'influencers': influencers,
        'search': search,
        'verified_only': verified_only,
        'featured_only': featured_only,
    }
    
    return render(request, 'influencers/influencers_list.html', context)


@require_http_methods(["GET"])
def influencer_detail_view(request, influencer_id):
    """
    Influencer detail page with collaboration request status
    """
    try:
        influencer = InfluencerProfile.objects.get(id=influencer_id)
    except InfluencerProfile.DoesNotExist:
        return render(request, '404.html', status=404)
    
    # Check if artisan is viewing and has sent collaboration request
    collaboration_status = None
    if request.user.is_authenticated and request.user.is_artisan():
        try:
            artisan = request.user.artisan_profile
            collaboration_status = CollaborationRequest.objects.filter(
                influencer=influencer,
                artisan=artisan
            ).first()
        except:
            collaboration_status = None
    
    context = {
        'influencer': influencer,
        'collaboration_status': collaboration_status,
    }
    
    return render(request, 'influencers/influencer_detail.html', context)

