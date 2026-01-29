from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from accounts.decorators import login_required
from products.models import Product
from .models import Cart, CartItem


@login_required
@require_http_methods(["GET"])
def cart_view(request):
    """
    View shopping cart
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
        'item_count': cart.get_item_count(),
    }
    
    return render(request, 'cart/cart.html', context)


@login_required
@require_http_methods(["POST"])
def add_to_cart_view(request, product_id):
    """
    Add product to cart
    """
    try:
        product = Product.objects.get(id=product_id, status='active')
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
        return redirect('products_list')
    
    if product.quantity_in_stock <= 0:
        messages.error(request, 'Product is out of stock.')
        return redirect('product_detail', product_id=product.id)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        messages.error(request, 'Invalid quantity.')
        return redirect('product_detail', product_id=product.id)
    
    if quantity > product.quantity_in_stock:
        messages.error(request, f'Only {product.quantity_in_stock} items available.')
        return redirect('product_detail', product_id=product.id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )
    
    if not item_created:
        # Update quantity if item already in cart
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    
    # Redirect to next page or cart
    next_page = request.POST.get('next', 'cart')
    return redirect(next_page)


@login_required
@require_http_methods(["POST"])
def remove_from_cart_view(request, product_id):
    """
    Remove product from cart
    """
    cart = Cart.objects.get(user=request.user)
    
    try:
        product = Product.objects.get(id=product_id)
        CartItem.objects.filter(cart=cart, product=product).delete()
        messages.success(request, 'Item removed from cart.')
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
    
    return redirect('cart')


@login_required
@require_http_methods(["POST"])
def update_cart_item_view(request, product_id):
    """
    Update quantity of product in cart
    """
    cart = Cart.objects.get(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    try:
        product = Product.objects.get(id=product_id)
        
        if quantity <= 0:
            CartItem.objects.filter(cart=cart, product=product).delete()
            messages.success(request, 'Item removed from cart.')
        elif quantity > product.quantity_in_stock:
            messages.error(request, f'Only {product.quantity_in_stock} items available.')
        else:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
    except (Product.DoesNotExist, CartItem.DoesNotExist):
        messages.error(request, 'Product not found.')
    
    return redirect('cart')


@login_required
@require_http_methods(["POST"])
def clear_cart_view(request):
    """
    Clear entire cart
    """
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared.')
    return redirect('cart')
