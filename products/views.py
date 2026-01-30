from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Review
from accounts.decorators import customer_required


@require_http_methods(["GET"])
def products_list_view(request):
    """
    List all products with search, filter, and sort
    """
    products = Product.objects.filter(status='active')
    categories = Category.objects.all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Category filter
    category = request.GET.get('category')
    if category:
        products = products.filter(category__id=category)
    # Always pass category as string for template comparison
    category_str = str(category) if category else ''
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=float(min_price))
    if max_price:
        products = products.filter(price__lte=float(max_price))
    
    # Eco-friendly filter
    eco_only = request.GET.get('eco', False)
    if eco_only:
        products = products.filter(is_eco_friendly=True)
    
    # In stock filter
    in_stock = request.GET.get('in_stock', False)
    if in_stock:
        products = products.filter(quantity_in_stock__gt=0)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)
    
    context = {
        'products': products,
        'categories': categories,
        'search': search,
        'category': category_str,
        'sort': sort,
    }
    
    return render(request, 'products/products_list.html', context)


@require_http_methods(["GET"])
def product_detail_view(request, product_id):
    """
    Product detail page
    """
    try:
        product = Product.objects.get(id=product_id, status='active')
    except Product.DoesNotExist:
        return render(request, '404.html', status=404)
    
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'can_review': request.user.is_authenticated and request.user.is_customer(),
    }
    
    return render(request, 'products/product_detail.html', context)


@login_required
@customer_required
@require_http_methods(["POST"])
def add_review_view(request, product_id):
    """
    Add/edit review for a product
    """
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
        return redirect('products_list')
    
    rating = request.POST.get('rating', 5)
    title = request.POST.get('title', '')
    comment = request.POST.get('comment', '')
    
    if not all([rating, title, comment]):
        messages.error(request, 'Please fill all review fields.')
        return redirect('product_detail', product_id=product.id)
    
    # Check if user already reviewed this product
    existing_review = Review.objects.filter(product=product, customer=request.user).first()
    
    if existing_review:
        # Update existing review
        existing_review.rating = int(rating)
        existing_review.title = title
        existing_review.comment = comment
        existing_review.save()
        messages.success(request, 'Review updated successfully!')
    else:
        # Create new review
        Review.objects.create(
            product=product,
            customer=request.user,
            rating=int(rating),
            title=title,
            comment=comment,
            is_verified_purchase=True,  # You should check actual purchase
        )
        messages.success(request, 'Review added successfully!')
    
    return redirect('product_detail', product_id=product.id)
