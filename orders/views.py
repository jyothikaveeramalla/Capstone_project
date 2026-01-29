from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from decimal import Decimal
from accounts.decorators import login_required
from cart.models import Cart, CartItem
from products.models import Product
from .models import Order, OrderItem, Shipment


@login_required
@require_http_methods(["GET"])
def orders_list_view(request):
    """
    View user's orders
    """
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'orders/orders_list.html', context)


@login_required
@require_http_methods(["GET"])
def order_detail_view(request, order_id):
    """
    View order details
    """
    try:
        order = Order.objects.get(id=order_id, customer=request.user)
    except Order.DoesNotExist:
        messages.error(request, 'Order not found.')
        return redirect('orders_list')
    
    order_items = order.orderitem_set.all()
    shipment = Shipment.objects.filter(order=order).first()
    
    context = {
        'order': order,
        'order_items': order_items,
        'shipment': shipment,
    }
    
    return render(request, 'orders/order_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def checkout_view(request):
    """
    Checkout page - collect shipping information
    """
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('products_list')
    
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('products_list')
    
    if request.method == 'POST':
        # Validate shipping information
        shipping_info = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'city': request.POST.get('city'),
            'state': request.POST.get('state'),
            'postal_code': request.POST.get('postal_code'),
            'country': request.POST.get('country'),
        }
        
        if not all(shipping_info.values()):
            messages.error(request, 'Please fill all shipping fields.')
            return redirect('checkout')
        
        # Store in session for confirmation
        request.session['shipping_info'] = shipping_info
        return redirect('order_confirm')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
    }
    
    return render(request, 'orders/checkout.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def order_confirm_view(request):
    """
    Order confirmation page
    """
    if 'shipping_info' not in request.session:
        return redirect('checkout')
    
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, 'Your cart is empty.')
        return redirect('products_list')
    
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('products_list')
    
    if request.method == 'POST':
        # Create order
        shipping_info = request.session['shipping_info']
        
        # Calculate totals
        subtotal = Decimal('0.00')
        for item in cart_items:
            subtotal += item.product.price * item.quantity
        
        shipping_cost = Decimal('10.00')  # Fixed shipping cost
        tax = (subtotal + shipping_cost) * Decimal('0.10')  # 10% tax
        total = subtotal + shipping_cost + tax
        
        # Create order
        order = Order.objects.create(
            customer=request.user,
            shipping_name=shipping_info['name'],
            shipping_email=shipping_info['email'],
            shipping_phone=shipping_info['phone'],
            shipping_address=shipping_info['address'],
            shipping_city=shipping_info['city'],
            shipping_state=shipping_info['state'],
            shipping_postal_code=shipping_info['postal_code'],
            shipping_country=shipping_info['country'],
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax=tax,
            total_amount=total,
            order_status='pending',
            payment_status='pending',
        )
        
        # Create order items
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                artisan=cart_item.product.artisan,
                product_name=cart_item.product.name,
                product_price=cart_item.product.price,
                quantity=cart_item.quantity,
                subtotal=cart_item.product.price * cart_item.quantity,
            )
            
            # Reduce product quantity
            cart_item.product.quantity_in_stock -= cart_item.quantity
            cart_item.product.save()
        
        # Clear cart
        cart.items.all().delete()
        
        # Clear session
        del request.session['shipping_info']
        
        messages.success(request, f'Order #{order.order_id} placed successfully!')
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': cart.get_total_price(),
        'shipping_info': request.session['shipping_info'],
    }
    
    return render(request, 'orders/order_confirm.html', context)
