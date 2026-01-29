# ROLE-BASED PERMISSIONS - INTEGRATION & FLOW GUIDE

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARTISAN EDGE PLATFORM                         │
│              Role-Based Access Control System                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ARTISAN WORKFLOW: Product Publishing                     │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │ 1. User Signs In                                         │  │
│  │    └─> Dashboard (role='artisan')                        │  │
│  │                                                            │  │
│  │ 2. Navigate to Products                                  │  │
│  │    └─> /products/                                        │  │
│  │    └─> See "Add Product" button (green)                  │  │
│  │                                                            │  │
│  │ 3. Click "Add Product"                                   │  │
│  │    └─> @login_required ✓                                 │  │
│  │    └─> @artisan_required ✓                               │  │
│  │    └─> GET /products/manage/add/                         │  │
│  │    └─> Display ProductForm                               │  │
│  │                                                            │  │
│  │ 4. Fill Product Form                                     │  │
│  │    ├─ name (required)                                    │  │
│  │    ├─ description (required)                             │  │
│  │    ├─ category (required)                                │  │
│  │    ├─ price (required, >= 0.01)                          │  │
│  │    ├─ quantity_in_stock (required, >= 0)                 │  │
│  │    ├─ image (required, valid image)                      │  │
│  │    └─ optional fields (material, dimensions, etc.)       │  │
│  │                                                            │  │
│  │ 5. Submit Form (POST)                                    │  │
│  │    └─> Server-side validation                            │  │
│  │    └─> If valid:                                         │  │
│  │        ├─> Create Product                                │  │
│  │        ├─> Link to current artisan                       │  │
│  │        │  product.artisan = request.user.artisan_profile │  │
│  │        ├─> Save image to media/products/                 │  │
│  │        └─> Atomic transaction (all or nothing)           │  │
│  │    └─> If invalid:                                       │  │
│  │        └─> Show error messages                           │  │
│  │                                                            │  │
│  │ 6. Success                                               │  │
│  │    ├─> Show success message                              │  │
│  │    ├─> Redirect to artisan's products page               │  │
│  │    └─> Product visible in listing                        │  │
│  │                                                            │  │
│  │ 7. Manage Products                                       │  │
│  │    └─> /products/manage/my/                              │  │
│  │    ├─ View all own products in table                     │  │
│  │    ├─ Search and filter by status                        │  │
│  │    ├─ Edit: Update product details                       │  │
│  │    │  └─> Ownership check: product.artisan.user == user │  │
│  │    └─> Delete: Soft delete (status='discontinued')       │  │
│  │       └─> Ownership check: product.artisan.user == user  │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ INFLUENCER WORKFLOW: Collaboration Requests              │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │ 1. User Signs In                                         │  │
│  │    └─> Dashboard (role='influencer')                     │  │
│  │                                                            │  │
│  │ 2. Browse Artisans                                       │  │
│  │    └─> /artisans/                                        │  │
│  │    └─> View artisan profiles                             │  │
│  │    └─> See "Request Collaboration" button (green)        │  │
│  │                                                            │  │
│  │ 3. Click "Request Collaboration"                         │  │
│  │    └─> @login_required ✓                                 │  │
│  │    └─> @influencer_required ✓                            │  │
│  │    └─> GET /collaborations/request/new/                  │  │
│  │    └─> Display CollaborationRequestForm                  │  │
│  │       └─> Pre-fill artisan (if from artisan page)        │  │
│  │                                                            │  │
│  │ 4. Fill Collaboration Form                               │  │
│  │    ├─ title (required, e.g., "Feature in my YouTube")    │  │
│  │    ├─ description (required, what you want to do)        │  │
│  │    ├─ proposed_terms (required, timeline & deliverables) │  │
│  │    ├─ commission_percentage (optional, %)                │  │
│  │    ├─ flat_rate (optional, ₹)                            │  │
│  │    └─ attachment (optional, media kit PDF)               │  │
│  │                                                            │  │
│  │ 5. Submit Form (POST)                                    │  │
│  │    └─> Server-side validation                            │  │
│  │    └─> Check for duplicates:                             │  │
│  │        ├─ SELECT * FROM collaborations_request           │  │
│  │        │  WHERE influencer_id = X AND artisan_id = Y     │  │
│  │        └─ If exists: Error "Already sent request"        │  │
│  │    └─> If valid:                                         │  │
│  │        ├─> Create CollaborationRequest                   │  │
│  │        ├─> Link to current influencer                    │  │
│  │        │  request.influencer = influencer_profile        │  │
│  │        ├─> Set status = 'pending'                        │  │
│  │        ├─> Save form fields                              │  │
│  │        └─> Atomic transaction                            │  │
│  │    └─> If invalid:                                       │  │
│  │        └─> Show error messages                           │  │
│  │                                                            │  │
│  │ 6. Success                                               │  │
│  │    ├─> Show success message                              │  │
│  │    ├─> Redirect to collaborations list                   │  │
│  │    └─> Request visible as 'pending'                      │  │
│  │                                                            │  │
│  │ 7. Track Status                                          │  │
│  │    └─> /collaborations/                                  │  │
│  │    ├─ View pending requests sent                         │  │
│  │    ├─ View accepted/rejected requests                    │  │
│  │    └─ See artisan response (if any)                      │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ARTISAN WORKFLOW: Manage Collaboration Requests          │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │ 1. Artisan Signs In                                      │  │
│  │    └─> Dashboard (role='artisan')                        │  │
│  │                                                            │  │
│  │ 2. View Collaborations                                   │  │
│  │    └─> /collaborations/                                  │  │
│  │    └─> See requests from influencers                     │  │
│  │    └─> Grouped: pending, accepted, rejected              │  │
│  │                                                            │  │
│  │ 3. Accept or Reject Request                              │  │
│  │    ├─> Click "Accept" or "Reject" button                 │  │
│  │    ├─> @login_required ✓                                 │  │
│  │    ├─> @artisan_required ✓                               │  │
│  │    ├─> GET /collaborations/request/<id>/accept/          │  │
│  │    └─> GET /collaborations/request/<id>/reject/          │  │
│  │                                                            │  │
│  │ 4. Optional: Add Response Message                        │  │
│  │    ├─ If accepting: "Let's discuss details on email"     │  │
│  │    └─ If rejecting: "Not aligned with my focus"          │  │
│  │                                                            │  │
│  │ 5. Update Status                                         │  │
│  │    ├─ status = 'accepted' or 'rejected'                  │  │
│  │    ├─ response_from_artisan = message                    │  │
│  │    ├─ responded_at = now()                               │  │
│  │    └─ Atomic transaction                                 │  │
│  │                                                            │  │
│  │ 6. Success                                               │  │
│  │    ├─> Show success message                              │  │
│  │    ├─> If accepted:                                      │  │
│  │    │   └─> Create ActiveCollaboration record             │  │
│  │    ├─> Email notification sent to influencer             │  │
│  │    └─> Redirect to collaborations list                   │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ ACCESS CONTROL: Decorators & Checks                      │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                            │  │
│  │ Request comes in                                         │  │
│  │    │                                                      │  │
│  │    ├─> Check: @login_required                            │  │
│  │    │   ├─ User authenticated? ✓                          │  │
│  │    │   └─ No? → Redirect to /signin/                     │  │
│  │    │                                                      │  │
│  │    ├─> Check: @artisan_required                          │  │
│  │    │   ├─ User.role == 'artisan'? ✓                      │  │
│  │    │   └─ No? → Redirect to /                            │  │
│  │    │           Show: "Access restricted to artisans only"│  │
│  │    │                                                      │  │
│  │    ├─> Check: Ownership (in view)                        │  │
│  │    │   ├─ product.artisan.user == request.user? ✓        │  │
│  │    │   └─ No? → Show error, don't allow edit/delete      │  │
│  │    │                                                      │  │
│  │    └─> View executes                                     │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## REQUEST FLOW DIAGRAMS

### Product Addition Flow
```
Artisan clicks "Add Product"
    ↓
GET /products/manage/add/ request
    ↓
Middleware: Check authentication ✓
    ↓
@login_required: User logged in? ✓
    ↓
@artisan_required: User role == 'artisan'? ✓
    ↓
@require_http_methods(["GET", "POST"]): Is GET? ✓
    ↓
add_product_view() executes
    ├─ Get ArtisanProfile for request.user
    ├─ Create empty ProductForm()
    └─ Render add_product.html with form
    ↓
Browser displays form
    ↓
Artisan fills form and submits (POST)
    ↓
POST /products/manage/add/ request
    ↓
Middleware: Check CSRF token ✓
    ↓
@login_required: User logged in? ✓
    ↓
@artisan_required: User role == 'artisan'? ✓
    ↓
@require_http_methods(["GET", "POST"]): Is POST? ✓
    ↓
add_product_view() handles POST
    ├─ Get ArtisanProfile
    ├─ Create ProductForm with POST data
    ├─ Validate form (price >= 0.01, image valid, etc.)
    ├─ If invalid: Show errors, re-render form
    └─ If valid:
        ├─ product = form.save(commit=False)
        ├─ product.artisan = artisan  ← Link to artisan
        ├─ product.save()
        ├─ Save image to media/products/
        ├─ Atomic transaction commits
        ├─ Show success message
        └─ Redirect to artisan_products page
    ↓
artisan_products_view() displays updated list
    ↓
Artisan sees their new product in the listing
```

### Collaboration Request Flow
```
Influencer clicks "Request Collaboration" (on artisan profile)
    ↓
GET /collaborations/request/new/?artisan_id=1 request
    ↓
@login_required: User logged in? ✓
    ↓
@influencer_required: User role == 'influencer'? ✓
    ↓
new_collaboration_request_view() executes
    ├─ Get InfluencerProfile for request.user
    ├─ Get ArtisanProfile from query params (or form)
    ├─ Create empty CollaborationRequestForm()
    └─ Render new_request.html with form & artisan pre-filled
    ↓
Browser displays form
    ↓
Influencer fills form and submits (POST)
    ↓
POST /collaborations/request/new/ request
    ↓
@login_required: User logged in? ✓
    ↓
@influencer_required: User role == 'influencer'? ✓
    ↓
new_collaboration_request_view() handles POST
    ├─ Get artisan_id from POST data
    ├─ Get ArtisanProfile (if not exists → error)
    ├─ Check for duplicate:
    │  SELECT * FROM collaborations_request
    │  WHERE influencer_id = X AND artisan_id = Y
    │  └─ If exists: Show error, don't create
    ├─ Create CollaborationRequest(
    │    influencer=influencer_profile,
    │    artisan=artisan_profile,
    │    title=form.title,
    │    description=form.description,
    │    proposed_terms=form.proposed_terms,
    │    status='pending'
    │  )
    ├─ Save attachment if provided
    ├─ Atomic transaction commits
    ├─ Show success message
    └─ Redirect to collaborations_list
    ↓
collaborations_list_view() displays with pending request
    ↓
Influencer sees their request marked as "pending"
    ↓
[Artisan receives notification]
    ↓
Artisan views collaborations dashboard
    ↓
Artisan clicks "Accept" or "Reject"
    ↓
GET /collaborations/request/<id>/accept/
    ↓
@login_required ✓
@artisan_required ✓
    ↓
accept_collaboration_view() updates status
    ├─ Get CollaborationRequest
    ├─ Verify artisan owns it: collab_req.artisan.user == request.user
    ├─ Update: status='accepted', responded_at=now()
    ├─ Add response message if provided
    ├─ Create ActiveCollaboration
    ├─ Atomic transaction commits
    ├─ Send email to influencer
    ├─ Show success message
    └─ Redirect to collaborations_list
    ↓
Influencer views dashboard
    ↓
Sees request status changed to "Accepted" ✓
```

---

## DATABASE RELATIONSHIPS

```
User (role = 'artisan')
    │
    ├─→ [OneToOne] ArtisanProfile
    │        │
    │        └─→ [OneToMany] Product
    │                 │
    │                 └─ name, price, image, status, etc.
    │
    └─→ [OneToMany] CollaborationRequest (as receiver)
             │
             ├─ influencer [FK] ← InfluencerProfile
             ├─ artisan [FK] ← ArtisanProfile (this user)
             └─ status: pending/accepted/rejected

User (role = 'influencer')
    │
    ├─→ [OneToOne] InfluencerProfile
    │        │
    │        └─→ [OneToMany] CollaborationRequest (as sender)
    │                 │
    │                 ├─ influencer [FK] ← InfluencerProfile (this user)
    │                 ├─ artisan [FK] ← ArtisanProfile
    │                 └─ status: pending/accepted/rejected
    │
    └─→ [OneToMany] ActiveCollaboration (as collaborator)
```

---

## VALIDATION LAYERS

```
Form Submission
    ↓
[LAYER 1: Client-Side HTML5 Validation]
├─ Required fields marked with 'required'
├─ Min/max values enforced
├─ Email/URL formats validated
└─ File type restrictions (images only)
    ↓
[LAYER 2: Form Validation (Django Forms)]
├─ ProductForm.is_valid()
│  ├─ name: CharField(max_length=255)
│  ├─ price: DecimalField(min_value=0.01)
│  ├─ image: ImageField(required=True)
│  └─ All fields checked
├─ CollaborationRequestForm.is_valid()
│  ├─ title: CharField(max_length=255)
│  ├─ description: TextField(required=True)
│  └─ No duplicates (unique_together)
└─ Errors returned to user
    ↓
[LAYER 3: Server-Side Logic]
├─ Ownership verification
│  ├─ product.artisan.user == request.user?
│  └─ collab_req.artisan.user == request.user? (for accept/reject)
├─ Duplicate check for collaborations
├─ File upload validation
└─ Database constraints
    ↓
[LAYER 4: Database Constraints]
├─ Foreign Key constraints (referential integrity)
├─ NOT NULL constraints
├─ UNIQUE constraints (price >= 0.01, duplicate requests)
└─ CHECK constraints (status values)
    ↓
Success or Rollback (Atomic Transaction)
```

---

## PERMISSION MATRIX WITH FLOW

```
┌────────────────┬──────────────┬──────────┬────────┬──────────────┐
│ Action         │ Artisan      │ Customer │Influencer│   Admin     │
├────────────────┼──────────────┼──────────┼────────┼──────────────┤
│ ADD PRODUCT    │              │          │        │              │
│ Check:         │              │          │        │              │
│ ├─ Logged In   │ YES ✓        │ YES ✓    │ YES ✓  │ YES ✓        │
│ ├─ Role Match  │ YES ✓        │ NO ✗     │ NO ✗   │ YES ✓ (ovr)  │
│ └─ Allow       │ ✅ ALLOWED   │ ❌ ERROR │❌ ERROR│ ✅ ALLOWED   │
├────────────────┼──────────────┼──────────┼────────┼──────────────┤
│ EDIT PRODUCT   │              │          │        │              │
│ Check:         │              │          │        │              │
│ ├─ Logged In   │ YES ✓        │ YES ✓    │ YES ✓  │ YES ✓        │
│ ├─ Role Match  │ YES ✓        │ NO ✗     │ NO ✗   │ YES ✓ (ovr)  │
│ ├─ Own Product │ YES ✓        │ -        │ -      │ YES ✓ (any)  │
│ └─ Allow       │ ✅ ALLOWED   │ ❌ ERROR │❌ ERROR│ ✅ ALLOWED   │
├────────────────┼──────────────┼──────────┼────────┼──────────────┤
│ DELETE PRODUCT │              │          │        │              │
│ Check:         │              │          │        │              │
│ ├─ Logged In   │ YES ✓        │ YES ✓    │ YES ✓  │ YES ✓        │
│ ├─ Role Match  │ YES ✓        │ NO ✗     │ NO ✗   │ YES ✓ (ovr)  │
│ ├─ Own Product │ YES ✓        │ -        │ -      │ YES ✓ (any)  │
│ └─ Allow       │ ✅ ALLOWED   │ ❌ ERROR │❌ ERROR│ ✅ ALLOWED   │
├────────────────┼──────────────┼──────────┼────────┼──────────────┤
│ SEND COLLAB    │              │          │        │              │
│ Check:         │              │          │        │              │
│ ├─ Logged In   │ YES ✓        │ YES ✓    │ YES ✓  │ YES ✓        │
│ ├─ Role Match  │ NO ✗         │ NO ✗     │ YES ✓  │ YES ✓ (ovr)  │
│ ├─ Not Dup     │ -            │ -        │ YES ✓  │ YES ✓        │
│ └─ Allow       │ ❌ ERROR     │ ❌ ERROR │✅ ALLOWED│ ✅ ALLOWED   │
├────────────────┼──────────────┼──────────┼────────┼──────────────┤
│ ACCEPT COLLAB  │              │          │        │              │
│ Check:         │              │          │        │              │
│ ├─ Logged In   │ YES ✓        │ YES ✓    │ YES ✓  │ YES ✓        │
│ ├─ Role Match  │ YES ✓        │ NO ✗     │ NO ✗   │ YES ✓ (ovr)  │
│ ├─ Own Request │ YES ✓        │ -        │ -      │ YES ✓ (any)  │
│ └─ Allow       │ ✅ ALLOWED   │ ❌ ERROR │❌ ERROR│ ✅ ALLOWED   │
└────────────────┴──────────────┴──────────┴────────┴──────────────┘

Legend:
✅ ALLOWED = User can perform action
❌ ERROR = Access denied, error message shown
✓ = Condition met
✗ = Condition not met
(ovr) = Override (admin/staff bypass role checks)
```

---

## ERROR HANDLING FLOW

```
Request enters view
    ↓
Try to process
    ├─ Error Type 1: Authentication
    │  └─ User not logged in
    │     └─ Redirect: /signin/?next=[current_url]
    │     └─ Message: "Please sign in first."
    │
    ├─ Error Type 2: Authorization (Role)
    │  └─ User role doesn't match
    │     └─ Redirect: /
    │     └─ Message: "Access restricted to [role]s only."
    │
    ├─ Error Type 3: Authorization (Ownership)
    │  └─ User doesn't own resource
    │     └─ Redirect: /
    │     └─ Message: "You don't have permission to [action] this resource."
    │
    ├─ Error Type 4: Validation
    │  └─ Form data invalid
    │     └─ Re-render form
    │     └─ Show field errors
    │     └─ Keep user-entered values
    │
    ├─ Error Type 5: Business Logic
    │  └─ e.g., duplicate collaboration request
    │     └─ Re-render form
    │     └─ Message: "You have already sent a request to this artisan."
    │
    └─ Error Type 6: Server Error
       └─ Unexpected exception
          └─ Atomic transaction rollback
          └─ Show: "Error [action]: [error_message]"
          └─ Log error for debugging
```

---

## SECURITY CHECKS IN ORDER

```
1. CSRF Token Validation
   ├─ Middleware: django.middleware.csrf.CsrfViewMiddleware
   ├─ Template: {% csrf_token %}
   └─ Protects against: Cross-Site Request Forgery

2. Authentication Check
   ├─ Decorator: @login_required
   ├─ Redirects to: /signin/
   └─ Protects against: Unauthorized access by anonymous users

3. Role-Based Authorization
   ├─ Decorator: @artisan_required / @influencer_required
   ├─ Redirects to: /
   └─ Protects against: Access by wrong role

4. Ownership Verification (in view)
   ├─ Check: product.artisan.user == request.user
   ├─ Redirects to: /
   └─ Protects against: Users editing other users' data

5. Form Validation
   ├─ Validator: ProductForm.is_valid()
   ├─ Checks: Type, length, format, constraints
   └─ Protects against: Invalid/malicious data

6. Database Constraints
   ├─ Constraint: unique_together(['influencer', 'artisan'])
   ├─ Constraint: CHECK (price >= 0.01)
   └─ Protects against: Database-level violations

7. Atomic Transactions
   ├─ Transaction: with transaction.atomic()
   ├─ Behavior: All-or-nothing
   └─ Protects against: Partial/inconsistent data
```

---

## COMPLETE IMPLEMENTATION CHECKLIST

### Backend
- ✅ @artisan_required decorator applied to product views
- ✅ @influencer_required decorator applied to collaboration views
- ✅ Ownership verification in edit/delete views
- ✅ Form validation (ProductForm, CollaborationRequestForm)
- ✅ Database constraints (unique_together for collaborations)
- ✅ Soft delete for products (status field)
- ✅ Atomic transactions for data integrity
- ✅ Error messages for all failure scenarios
- ✅ Admin interface configured

### Frontend
- ✅ "Add Product" button (artisans only)
- ✅ "Manage Products" button (artisans only)
- ✅ Edit/Delete buttons (owner only)
- ✅ "Request Collaboration" button (influencers only)
- ✅ Collaboration request form
- ✅ Status badges and indicators
- ✅ Search and filter functionality
- ✅ Responsive design
- ✅ Error message display
- ✅ Success message display

### Documentation
- ✅ ROLE_BASED_PERMISSIONS.md (comprehensive)
- ✅ ROLE_BASED_PERMISSIONS_QUICK_REF.md (quick reference)
- ✅ This file (integration & flow guide)

---

## NEXT STEPS FOR DEPLOYMENT

1. Run migrations
2. Create test accounts (artisan, influencer, customer, admin)
3. Test complete workflows
4. Configure email notifications (optional)
5. Set up media file handling
6. Deploy to production
7. Monitor error logs

---

This completes the role-based permissions implementation!
