# Quick Reference Guide - Signup & Role-Based Access Control

## 🚀 Quick Start

### For Users
1. **Sign Up**: http://127.0.0.1:8000/account/signup/
2. **Select Role**: Choose Customer, Artisan, or Influencer
3. **Auto-Redirect**: You'll be taken to your role-specific page

### For Artisans (Product Management)
```
/products/manage/my/              View your products
/products/manage/add/             Create new product
/products/manage/<id>/edit/       Edit product
/products/manage/<id>/delete/     Delete product (POST)
```

### For Developers
```
Use @artisan_required decorator to protect artisan-only views
Use @customer_required decorator for customer-only features
Use @login_required for general authentication
```

---

## 🔑 Key Files Reference

### Authentication & Roles
- **User Model**: `accounts/models.py` (Role choices, helper methods)
- **Decorators**: `accounts/decorators.py` (7 reusable decorators)
- **Signup View**: `accounts/views.py` (Role selection & redirect)

### Product Management
- **Views**: `products/product_management.py` (Add, edit, delete, list)
- **Forms**: `products/forms.py` (ProductForm with validation)
- **URLs**: `products/urls.py` (Product management routes)

### Templates
- **Signup**: `templates/auth/signup.html` (Card-based role selection)
- **Add/Edit**: `templates/products/add_product.html`, `edit_product.html`
- **Dashboard**: `templates/products/my_products.html`

---

## 🛡️ Protecting Your Views

### Option 1: Artisan Only
```python
from accounts.decorators import login_required, artisan_required

@login_required
@artisan_required
def my_artisan_view(request):
    # Only authenticated artisans can access
    artisan = ArtisanProfile.objects.get(user=request.user)
    pass
```

### Option 2: Any Specific Role
```python
from accounts.decorators import role_required

@role_required('influencer')
def my_influencer_view(request):
    # Only influencers can access
    pass
```

### Option 3: Owner or Admin
```python
from accounts.decorators import owner_or_admin_required, artisan_required

@artisan_required
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    
    # Verify ownership
    if product.artisan.user != request.user and not request.user.is_staff:
        return redirect('dashboard')  # Or use decorator
    
    # Allow edit
    pass
```

---

## 📋 Role Permissions Matrix

| Feature | Customer | Artisan | Influencer | Admin |
|---------|----------|---------|------------|-------|
| Browse Products | ✅ | ✅ | ✅ | ✅ |
| Add Products | ❌ | ✅ | ❌ | ✅ |
| Edit Own Products | ❌ | ✅ | ❌ | ✅ |
| Delete Own Products | ❌ | ✅ | ❌ | ✅ |
| Browse Artisans | ✅ | ✅ | ✅ | ✅ |
| Create Collaborations | ❌ | ❌ | ✅ | ✅ |
| Place Orders | ✅ | ✅ | ✅ | ✅ |
| Leave Reviews | ✅ | ✅ | ✅ | ✅ |

---

## 🔐 Security Checklist

- [ ] All product management views have `@artisan_required`
- [ ] Ownership verified before allow edit/delete
- [ ] Forms validate input on server (not just client)
- [ ] CSRF token on all forms
- [ ] No hardcoded role strings (use methods)
- [ ] Error messages don't leak information
- [ ] Redirects use named URLs ({% url 'name' %})
- [ ] Database transactions for atomic operations

---

## 🐛 Common Issues & Solutions

### Issue: User Can't Add Products
```python
# Check:
1. User is logged in (not None)
2. User.role == 'artisan'
3. ArtisanProfile exists for user
4. View has @artisan_required decorator

# Debug:
from django.contrib.auth import get_user
user = get_user(request)
print(user.role)  # Should be 'artisan'
print(user.is_artisan())  # Should be True
```

### Issue: Can Edit Other User's Product
```python
# Add ownership check:
if product.artisan.user != request.user and not request.user.is_staff:
    messages.error(request, 'You cannot edit this product')
    return redirect('my_products')
```

### Issue: Decorator Not Working
```python
# Order matters! Do this:
@login_required      # First
@artisan_required    # Then
def view(request):
    pass

# NOT this:
@artisan_required    # Won't work - login check happens in decorator
@login_required
def view(request):
    pass
```

---

## 📝 Common Code Patterns

### Create Protected View
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from accounts.decorators import login_required, artisan_required
from artisans.models import ArtisanProfile

@login_required
@artisan_required
@require_http_methods(["GET", "POST"])
def my_feature(request):
    """
    Feature description.
    
    Access: Artisans only
    Methods: GET, POST
    """
    # Get artisan profile
    artisan = get_object_or_404(ArtisanProfile, user=request.user)
    
    # Handle POST
    if request.method == 'POST':
        # Your logic here
        messages.success(request, 'Success message')
        return redirect('some_view')
    
    # Handle GET
    context = {'artisan': artisan}
    return render(request, 'template.html', context)
```

### Add Product Safely
```python
from django.db import transaction

@transaction.atomic
def create_product(artisan, form_data):
    """Create product with transaction safety."""
    product = form.save(commit=False)
    product.artisan = artisan  # Set on server, not client
    product.save()
    return product
```

### Verify Ownership
```python
def can_edit_product(user, product):
    """Check if user can edit product."""
    return product.artisan.user == user or user.is_staff

# In view:
if not can_edit_product(request.user, product):
    messages.error(request, 'You cannot edit this product')
    return redirect('my_products')
```

---

## 🧪 Testing Pattern

```python
from django.test import TestCase, Client
from accounts.models import User

class ProductManagementTest(TestCase):
    def setUp(self):
        # Create artisan user
        self.artisan = User.objects.create_user(
            username='artisan',
            email='artisan@test.com',
            role='artisan',
            password='test123'
        )
        
        # Create customer user
        self.customer = User.objects.create_user(
            username='customer',
            email='customer@test.com',
            role='customer',
            password='test123'
        )
        
        self.client = Client()
    
    def test_artisan_can_add_product(self):
        self.client.login(username='artisan', password='test123')
        response = self.client.get('/products/manage/add/')
        self.assertEqual(response.status_code, 200)
    
    def test_customer_cannot_add_product(self):
        self.client.login(username='customer', password='test123')
        response = self.client.get('/products/manage/add/')
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('Access restricted', str(response.content))
```

---

## 🔍 Debugging Commands

```python
# In Django shell (python manage.py shell)

# Check user role
from accounts.models import User
user = User.objects.get(username='someuser')
print(user.role)
print(user.is_artisan())

# Check artisan profile
from artisans.models import ArtisanProfile
artisan = ArtisanProfile.objects.get(user=user)
print(artisan.products.all())

# Check product access
from products.models import Product
product = Product.objects.get(id=1)
print(product.artisan.user)
print(product.artisan.user == user)  # True if user owns it
```

---

## 📚 Documentation

1. **ROLE_BASED_ACCESS_CONTROL.md** - Comprehensive role documentation
2. **SIGNUP_RBAC_IMPLEMENTATION.md** - Implementation summary
3. **IMPLEMENTATION_VERIFICATION.md** - Verification checklist
4. **This File** - Quick reference

---

## 🎓 Learning Path

1. **Start Here**: Read this quick reference
2. **Understand Roles**: Read ROLE_BASED_ACCESS_CONTROL.md
3. **See Implementation**: Check SIGNUP_RBAC_IMPLEMENTATION.md
4. **Review Code**: Look at actual files referenced
5. **Test Features**: Follow testing instructions
6. **Verify**: Use IMPLEMENTATION_VERIFICATION.md checklist

---

## 💡 Tips & Tricks

### Tip 1: Use User Methods
```python
# ✅ Good
if request.user.is_artisan():
    # do something

# ❌ Bad
if request.user.role == 'artisan':  # String comparison
```

### Tip 2: Always Verify Ownership
```python
# ✅ Good - verify server-side
if product.artisan.user != request.user:
    return HttpResponseForbidden()

# ❌ Bad - trust frontend
if request.POST.get('is_owner'):  # User can fake this
```

### Tip 3: Use Transactions
```python
# ✅ Good - all or nothing
with transaction.atomic():
    product = form.save(commit=False)
    product.artisan = artisan
    product.save()
    # If error happens, everything rolls back

# ❌ Bad - might save partial state
product = form.save(commit=False)
product.artisan = artisan
product.save()
```

### Tip 4: Clear Error Messages
```python
# ✅ Good
messages.error(request, 'You do not have permission to edit this product')

# ❌ Bad
messages.error(request, 'Error!')
messages.error(request, 'Access denied')  # Too vague
```

---

## 📞 Need Help?

1. **Decorator not working?** Check decorator order (login first)
2. **Can't find views?** They're in `products/product_management.py`
3. **Template missing?** Check `templates/products/` folder
4. **Form validation failing?** Check `products/forms.py`
5. **Role not saving?** Check `accounts/views.py` signup_view

---

**Last Updated**: January 29, 2026
**Status**: ✅ READY TO USE
**Support**: See documentation files for detailed help
