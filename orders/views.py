from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import transaction
from decimal import Decimal

from accounts.decorators import login_required
from cart.models import Cart
from products.models import Product
from .models import Order, OrderItem, Shipment


# ----------------------------
# Orders List
# ----------------------------

@login_required
@require_http_methods(["GET"])
def orders_list_view(request):
    orders = Order.objects.filter(customer=request.user).order_by("-created_at")

    return render(request, "orders/orders_list.html", {
        "orders": orders
    })


# ----------------------------
# Checkout
# ----------------------------

@login_required
@require_http_methods(["GET", "POST"])
def checkout_view(request):

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty.")
        return redirect("products_list")

    cart_items = cart.items.all()

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("products_list")


    if request.method == "POST":
        import logging
        logger = logging.getLogger("django.checkout")

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        pincode = request.POST.get("pincode", "").strip()

        logger.info(f"[CHECKOUT] User: {request.user}, Name: {full_name}, Email: {email}, Phone: {phone}")

        if not all([full_name, email, phone, address, city, state, pincode]):
            messages.error(request, "Please fill all shipping fields.")
            return render(request, "orders/checkout.html", {
                "cart_items": cart_items,
                "cart_total": cart.get_total_price()
            })

        # Server-side stock validation
        for item in cart_items:
            if item.quantity > item.product.quantity_in_stock:
                messages.error(request, f"Not enough stock for {item.product.name}. Only {item.product.quantity_in_stock} left.")
                logger.warning(f"[CHECKOUT] Stock error for {item.product.name}: requested {item.quantity}, in stock {item.product.quantity_in_stock}")
                return render(request, "orders/checkout.html", {
                    "cart_items": cart_items,
                    "cart_total": cart.get_total_price()
                })

        with transaction.atomic():
            order = Order.objects.create(
                customer=request.user,
                shipping_name=full_name,
                shipping_email=email,
                shipping_phone=phone,
                shipping_address=address,
                shipping_city=city,
                shipping_state=state,
                shipping_postal_code=pincode,
                shipping_country="India",
                subtotal=cart.get_total_price(),
                total_amount=cart.get_total_price(),
            )
            logger.info(f"[ORDER] Created order {order.order_id} for user {request.user}")

            for item in cart_items:
                artisan_user = None
                if item.product.artisan:
                    artisan_user = item.product.artisan.user

                oi = OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    artisan=artisan_user,
                    product_name=item.product.name,
                    product_price=item.product.price,
                    quantity=item.quantity,
                    subtotal=item.get_total_price(),
                )
                logger.info(f"[ORDER] Created OrderItem {oi.id} for product {item.product.name} (artisan: {artisan_user})")

                # Update product stock
                item.product.quantity_in_stock -= item.quantity
                if item.product.quantity_in_stock < 0:
                    item.product.quantity_in_stock = 0
                item.product.save()
                logger.info(f"[CHECKOUT] Stock updated for {item.product.name}: now {item.product.quantity_in_stock}")

            cart.clear()
            logger.info(f"[CHECKOUT] Order {order.order_id} placed by {request.user}")

        return redirect("order_success", order_id=order.id)

    return render(request, "orders/checkout.html", {
        "cart_items": cart_items,
        "cart_total": cart.get_total_price()
    })


# ----------------------------
# Order Success
# ----------------------------

@login_required
@require_http_methods(["GET"])
def order_success_view(request, order_id):

    try:
        order = Order.objects.get(id=order_id, customer=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect("checkout")

    order_items = order.items.all()

    return render(request, "orders/order_success.html", {
        "order": order,
        "order_items": order_items
    })


# ----------------------------
# Order Detail
# ----------------------------

@login_required
@require_http_methods(["GET"])
def order_detail_view(request, order_id):

    try:
        order = Order.objects.get(id=order_id, customer=request.user)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect("orders_list")

    order_items = order.orderitem_set.all()
    shipment = Shipment.objects.filter(order=order).first()

    return render(request, "orders/order_detail.html", {
        "order": order,
        "order_items": order_items,
        "shipment": shipment
    })
