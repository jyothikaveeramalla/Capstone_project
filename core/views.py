from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from products.models import Product, Category
from .models import PageContent, Testimonial, Contact, StatisticBlock


@require_http_methods(["GET"])
def home_view(request):
    """
    Home page view
    """
    featured_products = Product.objects.filter(status='active')[:6]
    categories = Category.objects.all()[:6]
    testimonials = Testimonial.objects.filter(is_published=True, is_featured=True)[:3]
    statistics = StatisticBlock.objects.all()
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'testimonials': testimonials,
        'statistics': statistics,
    }
    
    return render(request, 'pages/home.html', context)


@require_http_methods(["GET"])
def about_view(request):
    """
    About page view
    """
    try:
        page = PageContent.objects.get(page_name='about')
    except PageContent.DoesNotExist:
        page = None
    
    context = {
        'page': page,
    }
    
    return render(request, 'pages/about.html', context)


@require_http_methods(["GET", "POST"])
def contact_view(request):
    """
    Contact page view
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if all([name, email, subject, message]):
            Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
            )
            messages.success(request, 'Your message has been sent! We will reply soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill all required fields.')
    
    context = {}
    return render(request, 'pages/contact.html', context)
