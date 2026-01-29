from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import ArtisanProfile
from products.models import Product


@require_http_methods(["GET"])
def artisans_list_view(request):
    """
    List all artisans with search and filter
    """
    artisans = ArtisanProfile.objects.all()
    
    # Search by craft type or name
    search = request.GET.get('search', '')
    if search:
        artisans = artisans.filter(
            Q(craft_type__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search)
        )
    
    # Filter by featured
    featured_only = request.GET.get('featured', False)
    if featured_only:
        artisans = artisans.filter(is_featured=True)
    
    # Sort options
    sort = request.GET.get('sort', '-rating')
    artisans = artisans.order_by(sort)
    
    context = {
        'artisans': artisans,
        'search': search,
        'featured_only': featured_only,
    }
    
    return render(request, 'artisans/artisans_list.html', context)


@require_http_methods(["GET"])
def artisan_detail_view(request, artisan_id):
    """
    Artisan detail page
    """
    try:
        artisan = ArtisanProfile.objects.get(id=artisan_id)
    except ArtisanProfile.DoesNotExist:
        return render(request, '404.html', status=404)
    
    products = Product.objects.filter(artisan=artisan, status='active')
    
    context = {
        'artisan': artisan,
        'products': products,
    }
    
    return render(request, 'artisans/artisan_detail.html', context)


@require_http_methods(["GET"])
def artisan_products_view(request, artisan_id):
    """
    List products by a specific artisan
    """
    try:
        artisan = ArtisanProfile.objects.get(id=artisan_id)
    except ArtisanProfile.DoesNotExist:
        return render(request, '404.html', status=404)
    
    products = Product.objects.filter(artisan=artisan, status='active')
    
    # Filtering
    category = request.GET.get('category')
    if category:
        products = products.filter(category__id=category)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)
    
    context = {
        'artisan': artisan,
        'products': products,
    }
    
    return render(request, 'artisans/artisan_products.html', context)
