from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from artisans.models import ArtisanProfile
from influencers.models import InfluencerProfile
from .forms import UserSignUpForm, UserSignInForm, UserProfileForm, ArtisanProfileForm, InfluencerProfileForm
from .decorators import login_required

User = get_user_model()


@require_http_methods(["GET", "POST"])
@csrf_protect
def signup_view(request):
    """
    User registration view with role selection and role-based redirect.
    
    Roles:
    - customer: Redirects to marketplace
    - artisan: Redirects to artisan dashboard
    - influencer: Redirects to influencer dashboard
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create artisan or influencer profile if needed
            if user.role == 'artisan':
                ArtisanProfile.objects.create(user=user)
                profile_created = True
            elif user.role == 'influencer':
                InfluencerProfile.objects.create(user=user)
                profile_created = True
            else:
                profile_created = False
            
            # Auto-login after signup
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created.')
            
            # Role-based redirect
            if user.role == 'artisan':
                messages.info(request, 'Please complete your artisan profile to start selling.')
                return redirect('artisan_setup')
            elif user.role == 'influencer':
                messages.info(request, 'Please complete your influencer profile to start collaborating.')
                return redirect('influencer_setup')
            else:  # customer
                return redirect('products_list')
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserSignUpForm()
    
    return render(request, 'auth/signup.html', {'form': form})


@require_http_methods(["GET", "POST"])
@csrf_protect
def signin_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserSignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    
                    if remember_me:
                        request.session.set_expiry(1209600)  # 2 weeks
                    
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    
                    # Redirect to next page or dashboard
                    next_page = request.GET.get('next', 'dashboard')
                    return redirect(next_page)
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserSignInForm()
    
    return render(request, 'auth/signin.html', {'form': form})


@require_http_methods(["GET"])
def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
@require_http_methods(["GET", "POST"])
def profile_view(request):
    """
    User profile view - edit basic information
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'auth/profile.html', context)


@login_required
@require_http_methods(["GET"])
def dashboard_view(request):
    """
    Dashboard view - different for each role
    """
    context = {
        'user': request.user,
    }
    
    if request.user.is_artisan():
        try:
            artisan = ArtisanProfile.objects.get(user=request.user)
            context['artisan'] = artisan
            context['products_count'] = artisan.products.count()
        except ArtisanProfile.DoesNotExist:
            pass
        return render(request, 'dashboard/artisan_dashboard.html', context)
    
    elif request.user.is_influencer():
        try:
            influencer = InfluencerProfile.objects.get(user=request.user)
            context['influencer'] = influencer
        except InfluencerProfile.DoesNotExist:
            pass
        return render(request, 'dashboard/influencer_dashboard.html', context)
    
    else:  # Customer
        return render(request, 'dashboard/customer_dashboard.html', context)


@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def artisan_profile_setup(request):
    """
    Setup/edit artisan profile
    """
    if not request.user.is_artisan():
        messages.error(request, 'Only artisans can access this page.')
        return redirect('dashboard')
    
    try:
        artisan = ArtisanProfile.objects.get(user=request.user)
    except ArtisanProfile.DoesNotExist:
        artisan = ArtisanProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = ArtisanProfileForm(request.POST)
        if form.is_valid():
            # Update artisan profile using explicit fields on the model
            artisan.craft_type = form.cleaned_data.get('craft_type')
            artisan.description = form.cleaned_data.get('description')
            artisan.years_of_experience = form.cleaned_data.get('years_of_experience')
            artisan.workshop_location = form.cleaned_data.get('workshop_location')
            artisan.website = form.cleaned_data.get('website')

            artisan.instagram_handle = form.cleaned_data.get('instagram')
            artisan.facebook_link = form.cleaned_data.get('facebook')
            artisan.save()

            messages.success(request, 'Your artisan profile has been updated.')
            return redirect('dashboard')
    else:
        initial_data = {
            'craft_type': artisan.craft_type,
            'description': artisan.description,
            'years_of_experience': artisan.years_of_experience,
            'workshop_location': artisan.workshop_location,
            'website': artisan.website,
            'instagram': artisan.instagram_handle or '',
            'facebook': artisan.facebook_link or '',
        }
        form = ArtisanProfileForm(initial=initial_data)
    
    context = {
        'form': form,
        'artisan': artisan,
    }
    return render(request, 'artisan/profile_setup.html', context)


@login_required
@require_http_methods(["GET", "POST"])
@csrf_protect
def influencer_profile_setup(request):
    """
    Setup/edit influencer profile
    """
    if not request.user.is_influencer():
        messages.error(request, 'Only influencers can access this page.')
        return redirect('dashboard')
    
    try:
        influencer = InfluencerProfile.objects.get(user=request.user)
    except InfluencerProfile.DoesNotExist:
        influencer = InfluencerProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = InfluencerProfileForm(request.POST)
        if form.is_valid():
            # Update influencer profile using explicit fields on the model
            influencer.niche = form.cleaned_data.get('niche')
            influencer.bio = form.cleaned_data.get('bio')

            influencer.instagram_handle = form.cleaned_data.get('instagram_url')
            influencer.youtube_handle = form.cleaned_data.get('youtube_url')
            influencer.facebook_link = form.cleaned_data.get('facebook_url')
            influencer.twitter_handle = form.cleaned_data.get('twitter_url')

            # Set follower counts on platform-specific fields
            influencer.instagram_followers = form.cleaned_data.get('instagram_followers') or 0
            influencer.youtube_subscribers = form.cleaned_data.get('youtube_followers') or 0
            # Note: influencer model doesn't have facebook_followers/twitter_followers fields; use totals where available
            try:
                influencer.facebook_followers = form.cleaned_data.get('facebook_followers') or 0
            except Exception:
                pass
            try:
                influencer.twitter_followers = form.cleaned_data.get('twitter_followers') or 0
            except Exception:
                pass

            # Update aggregate follower_count if available
            total_followers = 0
            total_followers += influencer.instagram_followers or 0
            total_followers += influencer.youtube_subscribers or 0
            # include any platform-specific follower fields if present
            if hasattr(influencer, 'facebook_followers'):
                total_followers += influencer.facebook_followers or 0
            if hasattr(influencer, 'twitter_followers'):
                total_followers += influencer.twitter_followers or 0

            influencer.follower_count = total_followers
            influencer.collaboration_rate = form.cleaned_data.get('collaboration_rate') or 0
            influencer.save()

            messages.success(request, 'Your influencer profile has been updated.')
            return redirect('dashboard')
    else:
        initial_data = {
            'niche': influencer.niche,
            'bio': influencer.bio,
            'instagram_url': influencer.instagram_handle or '',
            'youtube_url': influencer.youtube_handle or '',
            'facebook_url': influencer.facebook_link or '',
            'twitter_url': influencer.twitter_handle or '',
            'instagram_followers': getattr(influencer, 'instagram_followers', 0),
            'youtube_followers': getattr(influencer, 'youtube_subscribers', 0),
            'facebook_followers': getattr(influencer, 'facebook_followers', 0),
            'twitter_followers': getattr(influencer, 'twitter_followers', 0),
            'collaboration_rate': influencer.collaboration_rate,
        }
        form = InfluencerProfileForm(initial=initial_data)
    
    context = {
        'form': form,
        'influencer': influencer,
    }
    return render(request, 'influencer/profile_setup.html', context)
