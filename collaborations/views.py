from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Q
from accounts.decorators import login_required, influencer_required, artisan_required
from artisans.models import ArtisanProfile
from .models import CollaborationRequest, ActiveCollaboration, CollaborationPost


@login_required
@require_http_methods(["GET"])
def collaborations_list_view(request):
    """
    List collaborations based on user role
    """
    if request.user.is_influencer():
        # Show influencer's collaboration requests and active collaborations
        requests = CollaborationRequest.objects.filter(influencer__user=request.user)
        active = ActiveCollaboration.objects.filter(influencer__user=request.user)
    elif request.user.is_artisan():
        # Show artisan's collaboration requests and active collaborations
        requests = CollaborationRequest.objects.filter(artisan__user=request.user)
        active = ActiveCollaboration.objects.filter(artisan__user=request.user)
    else:
        messages.error(request, 'Only artisans and influencers can view collaborations.')
        return redirect('dashboard')
    
    context = {
        'requests': requests,
        'active': active,
    }
    
    return render(request, 'collaborations/list.html', context)


@influencer_required
@require_http_methods(["GET", "POST"])
def new_collaboration_request_view(request):
    """
    Create new collaboration request (influencer to artisan)
    """
    from influencers.models import InfluencerProfile
    
    try:
        influencer = InfluencerProfile.objects.get(user=request.user)
    except InfluencerProfile.DoesNotExist:
        messages.error(request, 'Please complete your influencer profile first.')
        return redirect('influencer_setup')
    
    if request.method == 'POST':
        artisan_id = request.POST.get('artisan_id')
        
        try:
            artisan = ArtisanProfile.objects.get(id=artisan_id)
        except ArtisanProfile.DoesNotExist:
            messages.error(request, 'Artisan not found.')
            return redirect('artisans_list')
        
        # Check if request already exists
        existing = CollaborationRequest.objects.filter(
            influencer=influencer,
            artisan=artisan
        ).first()
        
        if existing:
            messages.error(request, 'You have already sent a request to this artisan.')
            return redirect('artisans_list')
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        proposed_terms = request.POST.get('proposed_terms')
        commission = request.POST.get('commission_percentage') or 0
        flat_rate = request.POST.get('flat_rate') or 0
        
        collab_req = CollaborationRequest.objects.create(
            influencer=influencer,
            artisan=artisan,
            title=title,
            description=description,
            proposed_terms=proposed_terms,
            commission_percentage=float(commission),
            flat_rate=float(flat_rate),
            status='pending',
        )
        
        messages.success(request, 'Collaboration request sent!')
        return redirect('collaborations_list')
    
    artisans = ArtisanProfile.objects.all()
    context = {
        'artisans': artisans,
    }
    
    return render(request, 'collaborations/new_request.html', context)


@login_required
@require_http_methods(["GET"])
def collaboration_request_detail_view(request, request_id):
    """
    View collaboration request details
    """
    try:
        collab_req = CollaborationRequest.objects.get(id=request_id)
    except CollaborationRequest.DoesNotExist:
        messages.error(request, 'Request not found.')
        return redirect('collaborations_list')
    
    # Check if user is involved
    if request.user.is_influencer():
        if collab_req.influencer.user != request.user:
            messages.error(request, 'You do not have access to this request.')
            return redirect('collaborations_list')
    elif request.user.is_artisan():
        if collab_req.artisan.user != request.user:
            messages.error(request, 'You do not have access to this request.')
            return redirect('collaborations_list')
    else:
        messages.error(request, 'Only artisans and influencers can view requests.')
        return redirect('dashboard')
    
    context = {
        'collab_req': collab_req,
    }
    
    return render(request, 'collaborations/request_detail.html', context)


@artisan_required
@require_http_methods(["POST"])
def accept_collaboration_view(request, request_id):
    """
    Artisan accepts collaboration request
    """
    try:
        collab_req = CollaborationRequest.objects.get(id=request_id)
    except CollaborationRequest.DoesNotExist:
        messages.error(request, 'Request not found.')
        return redirect('collaborations_list')
    
    try:
        artisan = ArtisanProfile.objects.get(user=request.user)
    except ArtisanProfile.DoesNotExist:
        messages.error(request, 'Artisan profile not found.')
        return redirect('dashboard')
    
    if collab_req.artisan != artisan:
        messages.error(request, 'You can only respond to your own requests.')
        return redirect('collaborations_list')
    
    if collab_req.status != 'pending':
        messages.error(request, 'This request has already been responded to.')
        return redirect('collab_request_detail', request_id=request_id)
    
    # Create active collaboration
    ActiveCollaboration.objects.create(
        influencer=collab_req.influencer,
        artisan=collab_req.artisan,
        collaboration_request=collab_req,
        title=collab_req.title,
        description=collab_req.description,
        financial_terms=collab_req.proposed_terms,
        status='active',
    )
    
    # Update request status
    collab_req.status = 'accepted'
    collab_req.save()
    
    messages.success(request, 'Collaboration accepted!')
    return redirect('collaborations_list')


@artisan_required
@require_http_methods(["POST"])
def reject_collaboration_view(request, request_id):
    """
    Artisan rejects collaboration request
    """
    try:
        collab_req = CollaborationRequest.objects.get(id=request_id)
    except CollaborationRequest.DoesNotExist:
        messages.error(request, 'Request not found.')
        return redirect('collaborations_list')
    
    try:
        artisan = ArtisanProfile.objects.get(user=request.user)
    except ArtisanProfile.DoesNotExist:
        messages.error(request, 'Artisan profile not found.')
        return redirect('dashboard')
    
    if collab_req.artisan != artisan:
        messages.error(request, 'You can only respond to your own requests.')
        return redirect('collaborations_list')
    
    if collab_req.status != 'pending':
        messages.error(request, 'This request has already been responded to.')
        return redirect('collab_request_detail', request_id=request_id)
    
    # Update request status
    collab_req.status = 'rejected'
    collab_req.response = request.POST.get('response', '')
    collab_req.save()
    
    messages.success(request, 'Collaboration request rejected.')
    return redirect('collaborations_list')


@login_required
@require_http_methods(["GET"])
def active_collaboration_detail_view(request, collab_id):
    """
    View active collaboration details
    """
    try:
        collaboration = ActiveCollaboration.objects.get(id=collab_id)
    except ActiveCollaboration.DoesNotExist:
        messages.error(request, 'Collaboration not found.')
        return redirect('collaborations_list')
    
    # Check if user is involved
    if request.user.is_influencer():
        if collaboration.influencer.user != request.user:
            messages.error(request, 'You do not have access to this collaboration.')
            return redirect('collaborations_list')
    elif request.user.is_artisan():
        if collaboration.artisan.user != request.user:
            messages.error(request, 'You do not have access to this collaboration.')
            return redirect('collaborations_list')
    else:
        messages.error(request, 'Only artisans and influencers can view collaborations.')
        return redirect('dashboard')
    
    posts = collaboration.collaborationpost_set.all()
    
    context = {
        'collaboration': collaboration,
        'posts': posts,
    }
    
    return render(request, 'collaborations/detail.html', context)


@influencer_required
@require_http_methods(["GET"])
def collaboration_posts_view(request, collab_id):
    """
    View posts from collaboration
    """
    try:
        collaboration = ActiveCollaboration.objects.get(id=collab_id)
    except ActiveCollaboration.DoesNotExist:
        messages.error(request, 'Collaboration not found.')
        return redirect('collaborations_list')
    
    from influencers.models import InfluencerProfile
    try:
        influencer = InfluencerProfile.objects.get(user=request.user)
    except InfluencerProfile.DoesNotExist:
        messages.error(request, 'Influencer profile not found.')
        return redirect('dashboard')
    
    if collaboration.influencer != influencer:
        messages.error(request, 'You do not have access to this collaboration.')
        return redirect('collaborations_list')
    
    posts = collaboration.collaborationpost_set.all()
    
    context = {
        'collaboration': collaboration,
        'posts': posts,
    }
    
    return render(request, 'collaborations/posts.html', context)


@influencer_required
@require_http_methods(["POST"])
def add_collaboration_post_view(request, collab_id):
    """
    Add post for collaboration
    """
    try:
        collaboration = ActiveCollaboration.objects.get(id=collab_id)
    except ActiveCollaboration.DoesNotExist:
        messages.error(request, 'Collaboration not found.')
        return redirect('collaborations_list')
    
    from influencers.models import InfluencerProfile
    try:
        influencer = InfluencerProfile.objects.get(user=request.user)
    except InfluencerProfile.DoesNotExist:
        messages.error(request, 'Influencer profile not found.')
        return redirect('dashboard')
    
    if collaboration.influencer != influencer:
        messages.error(request, 'You do not have access to this collaboration.')
        return redirect('collaborations_list')
    
    title = request.POST.get('title')
    content = request.POST.get('content')
    platform = request.POST.get('platform')
    url = request.POST.get('url')
    image = request.FILES.get('image')
    
    if not all([title, content, platform]):
        messages.error(request, 'Please fill all required fields.')
        return redirect('collab_posts', collab_id=collab_id)
    
    CollaborationPost.objects.create(
        collaboration=collaboration,
        title=title,
        content=content,
        platform=platform,
        url=url,
        image=image,
    )
    
    messages.success(request, 'Post added to collaboration!')
    return redirect('collab_posts', collab_id=collab_id)
