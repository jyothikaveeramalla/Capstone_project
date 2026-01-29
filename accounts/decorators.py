from functools import wraps
from django.contrib.auth.decorators import login_required as django_login_required
from django.shortcuts import redirect
from django.contrib import messages


def login_required(view_func):
    """
    Custom login required decorator that redirects to signin page.
    
    Usage: @login_required
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please sign in to access this page.')
            return redirect('signin')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(role):
    """
    Decorator to restrict views to specific user roles.
    
    Usage: @role_required('artisan')
    
    Args:
        role (str): The required user role ('customer', 'artisan', 'influencer', 'admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.warning(request, 'Please sign in first.')
                return redirect('signin')
            
            if request.user.role != role:
                messages.error(request, f'Access restricted: This page is only for {role}s.')
                return redirect('dashboard')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def artisan_required(view_func):
    """
    Decorator to restrict views to artisan users only.
    
    Usage: @artisan_required
    
    Redirects non-artisans to dashboard with error message.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please sign in first.')
            return redirect('signin')
        
        if not request.user.is_artisan():
            messages.error(request, 'Access restricted to artisans only.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def influencer_required(view_func):
    """
    Decorator to restrict views to influencer users only.
    
    Usage: @influencer_required
    
    Redirects non-influencers to dashboard with error message.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please sign in first.')
            return redirect('signin')
        
        if not request.user.is_influencer():
            messages.error(request, 'Access restricted to influencers only.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def customer_required(view_func):
    """
    Decorator to restrict views to customer users only.
    
    Usage: @customer_required
    
    Redirects non-customers to dashboard with error message.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please sign in first.')
            return redirect('signin')
        
        if not request.user.is_customer():
            messages.error(request, 'This page is for customers only.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """
    Decorator to restrict views to admin users only.
    
    Usage: @admin_required
    
    Redirects non-admins to dashboard with error message.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please sign in first.')
            return redirect('signin')
        
        if not request.user.is_staff:
            messages.error(request, 'Access restricted to administrators.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper


def owner_or_admin_required(view_func):
    """
    Decorator to restrict access to resource owner or admin.
    
    Usage: @owner_or_admin_required
    
    Assumes view receives an 'artisan_id' or 'product_id' kwarg.
    The user must either own the resource or be an admin.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please sign in first.')
            return redirect('signin')
        
        # Admin can access anything
        if request.user.is_staff or request.user.is_admin():
            return view_func(request, *args, **kwargs)
        
        # Regular users must own the resource
        if not request.user.is_artisan():
            messages.error(request, 'Only artisans can manage products.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    return wrapper
