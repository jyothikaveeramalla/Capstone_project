from django.shortcuts import render
from products.models import Product, Category


def marketplace_view(request):
    """Marketplace view: shows active products and category filtering"""
    products = Product.objects.filter(status='active').select_related('category', 'artisan')
    categories = Category.objects.all()

    # Category filtering via GET ?category=<id>
    category = request.GET.get('category')
    if category:
        products = products.filter(category__id=category)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': str(category) if category else ''
    }
    return render(request, 'marketplace.html', context)
