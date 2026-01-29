# Role-Based Access Control Documentation

## Overview

Artisan Edge implements a comprehensive role-based access control (RBAC) system to manage user permissions and restrict access to features based on user roles.

## User Roles

### 1. Customer
- **Role Value**: `customer`
- **Permissions**:
  - ✅ Browse products
  - ✅ View artisan profiles
  - ✅ Add products to cart
  - ✅ Place orders
  - ✅ Leave product reviews
  - ❌ Cannot manage products
  - ❌ Cannot create collaborations

### 2. Artisan
- **Role Value**: `artisan`
- **Permissions**:
  - ✅ Create, read, update, delete (CRUD) products
  - ✅ Manage product inventory
  - ✅ View orders from customers
  - ✅ Browse and respond to collaboration requests
  - ✅ All customer features
  - ❌ Cannot collaborate as influencer
  - ❌ Cannot access influencer features

### 3. Influencer
- **Role Value**: `influencer`
- **Permissions**:
  - ✅ Browse artisans
  - ✅ Create collaboration requests
  - ✅ View collaboration performance
  - ✅ Browse products
  - ✅ View influencer dashboard
  - ✅ All customer features
  - ❌ Cannot create products
  - ❌ Cannot manage artisan profile

### 4. Admin
- **Role Value**: `admin`
- **Permissions**:
  - ✅ All permissions across the system
  - ✅ Access Django admin panel
  - ✅ Manage users and roles
  - ✅ View system analytics
  - ✅ Moderate content

## Implementation Details

### User Model (`accounts/models.py`)

```python
class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('artisan', 'Artisan'),
        ('influencer', 'Influencer'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    
    # Role checking methods
    def is_artisan(self):
        return self.role == 'artisan'
    
    def is_influencer(self):
        return self.role == 'influencer'
    
    def is_customer(self):
        return self.role == 'customer'
```

### Access Control Decorators (`accounts/decorators.py`)

#### 1. Login Required
```python
@login_required
def protected_view(request):
    # Only authenticated users can access
    pass
```

#### 2. Role-Based Access
```python
@artisan_required
def artisan_only_view(request):
    # Only artisans can access
    pass

@influencer_required
def influencer_only_view(request):
    # Only influencers can access
    pass

@customer_required
def customer_only_view(request):
    # Only customers can access
    pass
```

#### 3. Generic Role Decorator
```python
@role_required('artisan')
def some_artisan_feature(request):
    # Specify role dynamically
    pass
```

#### 4. Owner or Admin
```python
@owner_or_admin_required
def edit_own_resource(request, product_id):
    # User must own the resource or be admin
    pass
```

## Product Management - Artisan Only

### URL Routes

```
GET  /products/manage/my/                    # List user's products
GET  /products/manage/add/                   # Show add product form
POST /products/manage/add/                   # Create new product
GET  /products/manage/<id>/edit/             # Show edit form
POST /products/manage/<id>/edit/             # Update product
POST /products/manage/<id>/delete/           # Delete product (soft delete)
```

### Protected Views

All product management views are protected with:
- **`@login_required`**: User must be logged in
- **`@artisan_required`**: User must have artisan role

```python
@login_required
@artisan_required
@require_http_methods(["GET", "POST"])
def add_product_view(request):
    # Only authenticated artisans can add products
    artisan = get_object_or_404(ArtisanProfile, user=request.user)
    # ... rest of implementation
```

### Ownership Verification

When editing or deleting products, the system verifies ownership:

```python
# Only creator or admin can edit
if product.artisan.user != request.user and not request.user.is_staff:
    messages.error(request, 'You do not have permission to edit this product.')
    return redirect('artisan_products', artisan_id=product.artisan.id)
```

## Sign-Up Flow

### Step 1: Role Selection
Users select their role during signup with visual card-based UI:
- 🛍️ Customer
- 🎨 Artisan
- ⭐ Influencer

### Step 2: Role-Based Redirect
After successful signup, users are redirected based on their role:

```python
if user.role == 'artisan':
    # Create artisan profile
    ArtisanProfile.objects.create(user=user)
    return redirect('artisan_setup')

elif user.role == 'influencer':
    # Create influencer profile
    InfluencerProfile.objects.create(user=user)
    return redirect('influencer_setup')

else:  # customer
    return redirect('products_list')
```

## Access Control Examples

### ✅ Artisan Can Access
```
GET  /products/manage/my/          (View own products)
GET  /products/manage/add/         (Add product form)
POST /products/manage/add/         (Create product)
GET  /products/manage/1/edit/      (Edit own product)
POST /products/manage/1/delete/    (Delete own product)
```

### ❌ Customer Cannot Access
```
GET  /products/manage/add/         → Redirected with error message
GET  /products/manage/my/          → Redirected with error message
POST /products/manage/add/         → Redirected with error message
```

### ❌ Non-Owner Cannot Edit Product
```
POST /products/manage/1/edit/      → Permission denied
     (Artisan B trying to edit Artisan A's product)
```

## Error Handling

### Unauthorized Access Messages
```python
# Not authenticated
"Please sign in to access this page."

# Wrong role
"Access restricted to artisans only."

# No permission
"You do not have permission to edit this product."
```

### Redirect Logic
```python
# Unauthenticated → Sign in page
# Wrong role → Dashboard
# No permission → Referring page or dashboard
```

## Best Practices

### 1. Always Verify Ownership
```python
# ✅ Good - Verify ownership on every action
if product.artisan.user != request.user and not request.user.is_staff:
    raise PermissionDenied()

# ❌ Bad - Trust frontend only
if request.POST.get('product_id'):  # Not safe
    product.delete()
```

### 2. Use Decorators Consistently
```python
# ✅ Good - Use decorators
@login_required
@artisan_required
def protected_view(request):
    pass

# ❌ Bad - Manual checks
def unprotected_view(request):
    if not request.user.is_authenticated:
        return redirect('signin')
```

### 3. Transaction Safety for Database Operations
```python
# ✅ Good - Use transactions
from django.db import transaction

with transaction.atomic():
    product = form.save(commit=False)
    product.artisan = artisan
    product.save()

# ❌ Bad - Multiple queries without transaction
product = form.save(commit=False)
product.artisan = artisan
product.save()
```

### 4. Clear Error Messages
```python
# ✅ Good - Specific message
messages.error(request, 'You do not have permission to edit this product.')

# ❌ Bad - Vague message
messages.error(request, 'Error!')
```

## Testing Access Control

### Test Case: Artisan Can Add Products
```python
def test_artisan_can_add_product(self):
    artisan_user = User.objects.create_user(
        username='artisan1',
        email='artisan@test.com',
        role='artisan'
    )
    ArtisanProfile.objects.create(user=artisan_user)
    
    client = Client()
    client.login(username='artisan1', password='test123')
    
    response = client.post('/products/manage/add/', {
        'name': 'Test Product',
        'description': 'Test',
        'price': '99.99',
        # ... other fields
    })
    
    assert response.status_code == 302  # Redirect after success
```

### Test Case: Customer Cannot Add Products
```python
def test_customer_cannot_add_product(self):
    customer_user = User.objects.create_user(
        username='customer1',
        email='customer@test.com',
        role='customer'
    )
    
    client = Client()
    client.login(username='customer1', password='test123')
    
    response = client.post('/products/manage/add/', {
        'name': 'Test Product',
        # ... fields
    })
    
    assert response.status_code == 302  # Redirect
    assert 'Access restricted' in messages(response)
```

## Common Issues & Solutions

### Issue: Decorator Order Matters
```python
# ✅ Correct - login_required first, then role checks
@login_required
@artisan_required
def view(request):
    pass

# ❌ Wrong - Role check before login check
@artisan_required
@login_required  # Never reached if not authenticated
def view(request):
    pass
```

### Issue: Mass Assignment Vulnerability
```python
# ❌ Bad - User can change artisan_id
product = form.save(commit=False)
product.artisan_id = request.POST.get('artisan_id')  # Dangerous
product.save()

# ✅ Good - Always assign from authenticated user
product = form.save(commit=False)
product.artisan = ArtisanProfile.objects.get(user=request.user)
product.save()
```

## Future Enhancements

1. **Permission-Based Access** (Django Permissions)
   ```python
   @permission_required('products.add_product')
   def add_product(request):
       pass
   ```

2. **Group-Based Roles**
   - Better scalability for complex permission hierarchies

3. **Audit Logging**
   - Track who accessed what and when

4. **Session Management**
   - Limit concurrent sessions
   - Force re-authentication for sensitive operations

5. **API Authentication**
   - JWT tokens for API access
   - API key management for integrations

## Summary

Artisan Edge implements a robust RBAC system that:
- ✅ Enforces role-based access at the decorator level
- ✅ Verifies ownership before allowing modifications
- ✅ Provides clear error messages and redirects
- ✅ Uses database transactions for data integrity
- ✅ Follows Django best practices
- ✅ Is scalable and maintainable

This ensures that users can only access and modify data they're authorized to work with, maintaining the security and integrity of the platform.
