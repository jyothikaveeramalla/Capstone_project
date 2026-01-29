# ROLE-BASED PERMISSIONS - QUICK REFERENCE

## What Was Implemented

### 1. **Artisan Product Publishing**
✅ Only artisans can add/edit/delete products
✅ Products automatically linked to logged-in artisan
✅ Product form includes: name, description, price, category, image, etc.
✅ Server-side validation on all fields
✅ Edit/Delete buttons visible only to product owner
✅ Soft delete (mark as discontinued, don't hard delete)
✅ "My Products" dashboard for management

### 2. **Influencer Collaboration Requests**
✅ Only influencers can send collaboration requests
✅ Cannot send duplicate requests to same artisan
✅ Show request status (pending/accepted/rejected)
✅ Artisans can accept or reject requests
✅ Form includes: title, description, terms, commission/rate, attachments
✅ "Request Collaboration" button on artisan profiles/products
✅ Influencers can track request status

### 3. **Access Control**
✅ @artisan_required decorator protects product views
✅ @influencer_required decorator protects collaboration views
✅ Ownership verification (can't edit/delete others' products)
✅ Unauthorized users redirected with error messages
✅ Admin can override all restrictions

### 4. **Frontend UI**
✅ "Add Product" button (visible only to artisans)
✅ "Request Collaboration" button (visible only to influencers)
✅ Edit/Delete product buttons (visible only to owner)
✅ "Manage Products" dashboard
✅ Collaboration request form
✅ Status indicators and badges

---

## HOW TO USE

### For Artisans:
1. Go to Products page
2. Click "Add Product" button (green, top right)
3. Fill in product details:
   - Name, description, category
   - Price and quantity
   - Upload product image
   - Optional: cost price, material, dimensions, eco-friendly flag
4. Click "Publish Product"
5. Manage products from "My Products" dashboard
   - Edit: Click edit button
   - Delete: Click delete button (soft delete)
   - View: Click product card

### For Influencers:
1. Browse artisans in the "Artisans" section
2. View artisan profile or products
3. Click "Request Collaboration" button
4. Fill collaboration request form:
   - Select artisan (if from form page)
   - Enter collaboration title
   - Describe what you want to do
   - Propose terms and timeline
   - Optional: commission/flat rate
   - Optional: attach media kit
5. Submit request
6. Track status in Collaborations dashboard
7. View artisan response

---

## BUTTONS & VISIBILITY

| Button | Who Sees | Where | Color |
|--------|----------|-------|-------|
| "Add Product" | Artisans | Products list, My Products | Green |
| "Manage Products" | Artisan (own) | Their product listing | Blue |
| Edit (product) | Artisan (own) | Product card overlay | Yellow |
| Delete (product) | Artisan (own) | Product card overlay | Red |
| "Request Collaboration" | Influencers | Artisan profile/products | Green |
| "Manage Requests" | Influencers/Artisans | Collaborations dashboard | Blue |

---

## KEY FILES

| File | Purpose | Status |
|------|---------|--------|
| `products/product_management.py` | Add/edit/delete views | ✅ Complete |
| `products/forms.py` | Product form with validation | ✅ Complete |
| `collaborations/views.py` | Collaboration request views | ✅ Complete |
| `accounts/decorators.py` | Role-based decorators | ✅ Complete |
| `templates/products/add_product.html` | Add product form | ✅ Complete |
| `templates/products/edit_product.html` | Edit product form | ✅ Complete |
| `templates/products/my_products.html` | Management dashboard | ✅ Complete |
| `templates/artisans/artisan_products.html` | Artisan products list | ✅ Updated |
| `templates/artisans/artisan_detail.html` | Artisan profile | ✅ Updated |
| `templates/collaborations/new_request.html` | Collaboration form | ✅ Complete |

---

## DECORATORS EXPLAINED

### @artisan_required
```python
@login_required
@artisan_required
def add_product_view(request):
    # Only artisans can add products
    # Redirects non-artisans to dashboard with error
```

### @influencer_required
```python
@login_required
@influencer_required
def new_collaboration_request_view(request):
    # Only influencers can send requests
    # Redirects non-influencers to dashboard with error
```

### @login_required
```python
@login_required
def products_list_view(request):
    # Must be authenticated
    # Redirects anonymous users to sign-in
```

---

## OWNERSHIP VERIFICATION

### Products
```python
# Can only edit/delete own products
if product.artisan.user != request.user and not request.user.is_staff:
    # Deny access
```

### Collaboration Requests
```python
# Only sender can cancel request
if collab_req.influencer.user != request.user and not request.user.is_staff:
    # Deny access
    
# Only receiver can accept/reject
if collab_req.artisan.user != request.user and not request.user.is_staff:
    # Deny access
```

---

## ERROR MESSAGES

### Artisan Access
- "Access restricted to artisans only."
- "Please sign in first."
- "You do not have permission to edit this product."

### Influencer Access
- "Access restricted to influencers only."
- "Please sign in first."
- "You have already sent a request to this artisan."

### Form Validation
- "Price must be at least 0.01"
- "This field is required."
- "Please upload a valid image file"

---

## FORM VALIDATION

### Product Form (Server-Side)
✅ Name: required, max 255 chars
✅ Description: required
✅ Price: required, min 0.01
✅ Category: required
✅ Image: required, valid image format
✅ Quantity: required, min 0
✅ Status: required, must be active/inactive/discontinued

### Collaboration Request Form (Server-Side)
✅ Title: required, max 255 chars
✅ Description: required
✅ Proposed Terms: required
✅ Artisan: required, must exist
✅ No duplicate requests (unique constraint)
✅ Commission/Rate: optional, must be numeric if provided

---

## DATABASE CONSTRAINTS

### Product Model
- `artisan` ForeignKey (required) - Links to ArtisanProfile
- `status` CharField - Soft delete using status field
- All prices validated as Decimal(10,2)

### CollaborationRequest Model
- `influencer` ForeignKey (required) - Sender
- `artisan` ForeignKey (required) - Receiver
- `unique_together = ['influencer', 'artisan']` - Prevents duplicates
- `status` CharField - Tracks request lifecycle

---

## TESTING

### Quick Test Checklist
- [ ] Create artisan account
- [ ] Try adding product → Should work
- [ ] Create influencer account
- [ ] Try adding product → Should fail with error
- [ ] Try requesting collaboration → Should work
- [ ] As influencer, view artisan profile
- [ ] Try "Request Collaboration" → Should work
- [ ] As artisan, try requesting collaboration → Should fail
- [ ] Try viewing "Add Product" page directly → Should redirect
- [ ] Check messages for success/errors

---

## IMPORTANT NOTES

⚠️ **Soft Delete**: Products are marked as 'discontinued', not hard deleted. They can be restored in admin.

⚠️ **Ownership**: Always verify user owns the resource before allowing edit/delete.

⚠️ **Decorators**: Stack decorators in correct order:
```python
@login_required       # First: check authentication
@artisan_required     # Second: check role
@require_http_methods(["GET", "POST"])  # Third: check HTTP method
def my_view(request):
    pass
```

⚠️ **Transactions**: All product operations use atomic transactions for data integrity.

✅ **CSRF Protection**: All POST forms include {% csrf_token %}.

✅ **Admin Override**: Staff/admin users can edit any product or manage requests.

---

## URLS REFERENCE

**Artisan Product Management**:
- GET/POST `/products/manage/add/` - Add product
- GET/POST `/products/manage/<id>/edit/` - Edit product
- POST `/products/manage/<id>/delete/` - Delete product
- GET `/products/manage/my/` - My products dashboard

**Influencer Collaboration**:
- GET/POST `/collaborations/request/new/` - Send collaboration request
- GET/POST `/collaborations/request/<id>/accept/` - Accept request
- GET/POST `/collaborations/request/<id>/reject/` - Reject request
- GET `/collaborations/` - View all collaborations

**Public Views**:
- GET `/products/` - Browse products
- GET `/products/<id>/` - Product detail
- GET `/artisans/` - Browse artisans
- GET `/artisans/<id>/` - Artisan profile
- GET `/artisans/<id>/products/` - Artisan's products

---

## NEXT STEPS (Optional Enhancements)

1. **Email Notifications**: Send emails on product added, collaboration request sent/accepted/rejected
2. **Analytics**: Track product views, collaboration success rate
3. **Reviews**: Allow customers to review products and artisans
4. **Messaging**: In-app messaging for collaboration negotiation
5. **Product Analytics**: Views, clicks, conversion rate for artisans
6. **Bulk Operations**: Upload multiple products at once

---

## PRODUCTION CHECKLIST

- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Configure media directory permissions
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up email backend
- [ ] Test file uploads
- [ ] Test all decorators
- [ ] Verify ownership checks
- [ ] Test with multiple users
- [ ] Performance test large product lists

---

For detailed documentation, see: `ROLE_BASED_PERMISSIONS.md`
