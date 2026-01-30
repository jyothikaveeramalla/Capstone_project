# Code Citations

## License: unknown
https://github.com/siddhi117/Shift-Planner/tree/d7fedf75240a302fc308e04d327830fb1e584b1a/admin.py

```
)
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').
```


## License: unknown
https://github.com/daveheena/ShiftPlanner/tree/043a62918170b6ca5f355cb86e1399ec64996cde/admin.py

```
request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
```

# views.py

from django.shortcuts import render, redirect
from .models import Order, OrderItem, Product
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

@login_required
def checkout_view(request):
    cart = Cart(request)
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode')

        if not all([full_name, phone, address, city, state, pincode]):
            error_message = "Please fill all shipping fields"
        else:
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                address=address,
                city=city,
                state=state,
                pincode=pincode,
            )

            # For each cart item, create OrderItem with correct artisan (User)
            for item in cart:
                product = item['product']
                # Get the artisan user from the product's artisan profile
                artisan_profile = getattr(product, 'artisan', None)
                artisan_user = None
                if artisan_profile and hasattr(artisan_profile, 'user'):
                    artisan_user = artisan_profile.user

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=item['price'],
                    artisan=artisan_user,  # Must be a User instance
                )

            cart.clear()
            return redirect('orders:order_success', order_id=order.id)

    return render(request, 'checkout.html')