"""
Product Management Views - Artisan Only

This module handles product creation, editing, and deletion.
Only authenticated artisans can access these views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from accounts.decorators import artisan_required
from artisans.models import ArtisanProfile
from .models import Product, Category
from .forms import ProductForm


def user_can_edit_product(user, product):
    """
    Check if user can edit a product.
    User can edit if:
    1. They are the original artisan who created it
    2. They are part of the team that owns the product
    3. They are a staff member
    """
    if user.is_staff:
        return True
    
    # Check if user is the original artisan
    if product.artisan.user == user:
        return True
    
    # Check if product belongs to a team and user is a team member
    if product.team and product.team.has_member(user):
        return True
    
    return False


@login_required
@artisan_required
@require_http_methods(["GET", "POST"])
def add_product_view(request):
    """
    Create a new product (Artisan-only).
    
    GET: Display the product creation form
    POST: Save the new product
    
    Access: Only authenticated artisans can create products
    Products are created as team products if the artisan is part of a team
    """
    # Get the artisan profile for the current user
    artisan = get_object_or_404(ArtisanProfile, user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    product = form.save(commit=False)
                    product.artisan = artisan
                    # If artisan belongs to a team, assign the product to the team
                    if artisan.team:
                        product.team = artisan.team
                    product.save()
                    
                    messages.success(
                        request, 
                        f'Product "{product.name}" has been added successfully!'
                    )
                    return redirect('my_products')
            except Exception as e:
                messages.error(request, f'Error creating product: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm()
    
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'categories': categories,
        'page_title': 'Add New Product',
        'artisan': artisan,
    }
    
    return render(request, 'products/add_product.html', context)


@login_required
@artisan_required
@require_http_methods(["GET", "POST"])
def edit_product_view(request, product_id):
    """
    Edit an existing product (Artisan-only).
    
    GET: Display the product edit form
    POST: Save the edited product
    
    Access: Only the artisan who created the product, team members, or admins can edit
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Verify permissions
    if not user_can_edit_product(request.user, product):
        messages.error(request, 'You do not have permission to edit this product.')
        return redirect('my_products')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                with transaction.atomic():
                    product = form.save()
                    messages.success(
                        request, 
                        f'Product "{product.name}" has been updated successfully!'
                    )
                    return redirect('my_products')
            except Exception as e:
                messages.error(request, f'Error updating product: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ProductForm(instance=product)
    
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'product': product,
        'categories': categories,
        'page_title': f'Edit {product.name}',
    }
    
    return render(request, 'products/edit_product.html', context)


@login_required
@artisan_required
@require_http_methods(["POST"])
def delete_product_view(request, product_id):
    """
    Delete a product (Artisan-only).
    
    Access: Only the artisan who created the product, team members, or admins can delete
    Soft delete: Sets status to 'discontinued' instead of hard delete
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Verify permissions
    if not user_can_edit_product(request.user, product):
        messages.error(request, 'You do not have permission to delete this product.')
        return redirect('my_products')
    
    product_name = product.name
    
    try:
        with transaction.atomic():
            # Soft delete: mark as discontinued instead of hard delete
            product.status = 'discontinued'
            product.save()
            
            messages.success(
                request, 
                f'Product "{product_name}" has been deleted.'
            )
    except Exception as e:
        messages.error(request, f'Error deleting product: {str(e)}')
    
    return redirect('my_products')


@login_required
@artisan_required
@require_http_methods(["GET"])
def my_products_view(request):
    """
    View all products created by the current artisan or their team (Artisan-only).
    
    Shows:
    - Products created directly by the artisan
    - Products created by their team members (if part of a team)
    
    Access: Only authenticated artisans can view their own products
    """
    artisan = get_object_or_404(ArtisanProfile, user=request.user)
    
    # Get products created by this artisan
    products = Product.objects.filter(artisan=artisan).order_by('-created_at')
    
    # If artisan is part of a team, also get team products
    if artisan.team:
        team_products = Product.objects.filter(team=artisan.team).order_by('-created_at')
        # Combine queries - union to avoid duplicates
        products = products.union(team_products).order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status', 'all')
    if status_filter != 'all':
        products = products.filter(status=status_filter)
    
    # Search
    search = request.GET.get('search', '')
    if search:
        products = products.filter(name__icontains=search)
    
    context = {
        'products': products,
        'artisan': artisan,
        'status_filter': status_filter,
        'search': search,
        'page_title': 'My Products',
        'is_team_member': artisan.team is not None,
        'team': artisan.team,
    }
    
    return render(request, 'products/my_products.html', context)
