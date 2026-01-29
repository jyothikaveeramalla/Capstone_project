# INFLUENCER SYSTEM - ARCHITECTURE & RELATIONSHIPS

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ARTISAN EDGE PLATFORM                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                     INFLUENCER SYSTEM                           │  │
│  ├────────────────────────────────────────────────────────────────┤  │
│  │                                                                  │  │
│  │  1. NAVIGATION                                                  │  │
│  │     └─> "Influencers" link in base.html                        │  │
│  │                                                                  │  │
│  │  2. INFLUENCER DISCOVERY                                        │  │
│  │     ├─> /influencers/              [List all influencers]      │  │
│  │     │   ├─ Search by niche/name/bio                            │  │
│  │     │   ├─ Filter (verified, featured)                         │  │
│  │     │   ├─ Sort (rating, followers, collaborations)            │  │
│  │     │   └─ View Profile button                                 │  │
│  │     │                                                            │  │
│  │     └─> /influencers/<id>/        [Influencer profile detail]  │  │
│  │         ├─ Full bio and details                                 │  │
│  │         ├─ Social media links                                   │  │
│  │         ├─ Statistics (rating, followers, collaborations)       │  │
│  │         └─ Collaboration request status (for artisans)          │  │
│  │                                                                  │  │
│  │  3. COLLABORATION SYSTEM                                        │  │
│  │     ├─> Influencer Profile Model                               │  │
│  │     │   └─ Links to User (1:1)                                 │  │
│  │     │                                                            │  │
│  │     ├─> Collaboration Request Model                            │  │
│  │     │   ├─ influencer (FK → InfluencerProfile)                 │  │
│  │     │   ├─ artisan (FK → ArtisanProfile)                       │  │
│  │     │   ├─ status (pending/accepted/rejected/cancelled)         │  │
│  │     │   └─ unique_together constraint                          │  │
│  │     │                                                            │  │
│  │     └─> Collaboration Request Flow                             │  │
│  │         /collaborations/request/new/      [Influencer-only]    │  │
│  │         /collaborations/request/<id>/accept/  [Artisan-only]   │  │
│  │         /collaborations/request/<id>/reject/  [Artisan-only]   │  │
│  │                                                                  │  │
│  │  4. ACCESS CONTROL                                              │  │
│  │     ├─ @login_required        → Must be authenticated          │  │
│  │     ├─ @influencer_required   → Must be influencer             │  │
│  │     ├─ @artisan_required      → Must be artisan                │  │
│  │     └─ Decorators from accounts/decorators.py                  │  │
│  │                                                                  │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Model Relationships

```
                        ┌──────────────┐
                        │     User     │
                        ├──────────────┤
                        │ id (PK)      │
                        │ email        │
                        │ first_name   │
                        │ last_name    │
                        │ role *       │
                        │ created_at   │
                        └──────┬───────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
         (1:1)  │       (1:1)  │       (1:1)  │
                │              │              │
         ┌──────▼────────┐ ┌──▼─────────────┐ ┌──▼──────────────┐
         │InfluencerProf.│ │ ArtisanProfile │ │ CustomerProfile │
         ├───────────────┤ ├────────────────┤ ├─────────────────┤
         │ id (PK)       │ │ id (PK)        │ │ id (PK)         │
         │ user (FK) *   │ │ user (FK) *    │ │ user (FK) *     │
         │ niche         │ │ craft_type     │ │ preferences     │
         │ bio           │ │ description    │ │ address         │
         │ instagram     │ │ years_exp      │ │ phone           │
         │ youtube       │ │ rating         │ │ created_at      │
         │ followers     │ │ products       │ │ updated_at      │
         │ rating        │ │ created_at     │ │                 │
         │ collab_rate   │ │ updated_at     │ │                 │
         │ created_at    │ │                │ │                 │
         └────┬──────────┘ └────┬───────────┘ └─────────────────┘
              │                │
              │ (1:N) sends    │ (1:N) receives
              │ requests to    │ requests from
              │                │
              └────────┬───────┘
                       │
             ┌─────────▼──────────────┐
             │ CollaborationRequest   │
             ├───────────────────────┤
             │ id (PK)               │
             │ influencer (FK) *     │ ◄─── Influencer
             │ artisan (FK) *        │ ◄─── Artisan
             │ title                 │
             │ description           │
             │ proposed_terms        │
             │ commission_%          │
             │ flat_rate             │
             │ status *              │ (pending/accepted/rejected/cancelled)
             │ requested_at          │
             │ responded_at          │
             │ created_at            │
             │ updated_at            │
             │                       │
             │ unique_together:      │
             │ (influencer, artisan) │ ← Prevents duplicate requests
             └───────────────────────┘

Legend:
  PK   = Primary Key
  FK   = Foreign Key
  1:1  = One-to-One relationship
  1:N  = One-to-Many relationship
  *    = Important/Required field
```

---

## User Role Access Matrix

```
┌──────────────────────────────────────────────────────────────────────┐
│                        FEATURE ACCESS BY ROLE                         │
├──────────────────────┬────────┬──────────┬────────────┬──────────────┤
│ Feature              │ Public │ Customer │   Artisan  │ Influencer   │
├──────────────────────┼────────┼──────────┼────────────┼──────────────┤
│ Browse Influencers   │   ✅   │    ✅    │     ✅     │     ✅       │
│ View Influencer      │   ✅   │    ✅    │     ✅     │     ✅       │
│ Profile              │        │          │            │              │
├──────────────────────┼────────┼──────────┼────────────┼──────────────┤
│ Browse Artisans      │   ✅   │    ✅    │     ✅     │     ✅       │
│ View Artisan Profile │   ✅   │    ✅    │     ✅     │     ✅       │
├──────────────────────┼────────┼──────────┼────────────┼──────────────┤
│ View Products        │   ✅   │    ✅    │     ✅     │     ✅       │
│ Add to Cart          │   ❌   │    ✅    │     ❌     │     ❌       │
│ Checkout             │   ❌   │    ✅    │     ❌     │     ❌       │
├──────────────────────┼────────┼──────────┼────────────┼──────────────┤
│ Send Collab Request  │   ❌   │    ❌    │     ✅     │     ❌       │
│ Receive Collab Req   │   ❌   │    ❌    │     ✅     │     ❌       │
│ Accept/Reject Req    │   ❌   │    ❌    │     ✅     │     ❌       │
│ View Dashboard       │   ❌   │    ✅    │     ✅     │     ✅       │
│ Manage Collaborations│   ❌   │    ❌    │     ✅     │     ✅       │
├──────────────────────┼────────┼──────────┼────────────┼──────────────┤
│ Create/Edit Products │   ❌   │    ❌    │     ✅     │     ❌       │
│ View Orders          │   ❌   │    ✅    │     ✅     │     ❌       │
│ Admin Panel          │   ❌   │    ❌    │     ❌     │     ❌       │
└──────────────────────┴────────┴──────────┴────────────┴──────────────┘

✅ = Allowed
❌ = Denied
```

---

## Request Flow Diagram

### 1. Influencer Discovery Flow
```
User Visits /influencers/
        │
        ├─> influencers_list_view()
        │   ├─ Get all InfluencerProfile objects
        │   ├─ Apply search filters
        │   ├─ Apply sorting
        │   └─ Render influencers_list.html
        │
        ├─ User clicks "View Profile"
        │
        └─> influencer_detail_view(influencer_id)
            ├─ Get InfluencerProfile by ID
            ├─ Check if artisan viewing (check collaboration status)
            └─ Render influencer_detail.html
```

### 2. Collaboration Request Flow
```
Artisan User (logged in)
        │
        ├─> Visits /influencers/<id>/
        │   └─ Sees "Request Collaboration" button
        │
        ├─> Clicks "Request Collaboration"
        │   └─ Redirects to /collaborations/request/new/
        │
        ├─> new_collaboration_request_view() [influencer_required decorator]
        │   ├─ Check user is influencer ✓
        │   ├─ Render collaboration request form
        │   │  (Select artisan, title, description, terms, etc.)
        │   │
        │   └─> (GET) Form displayed
        │
        ├─> User fills form and submits (POST)
        │
        ├─> new_collaboration_request_view() handles POST
        │   ├─ Get artisan by ID
        │   ├─ Check for duplicate request
        │   │   └─ If exists: Show error "Already sent request"
        │   ├─ Create CollaborationRequest object
        │   │   ├─ influencer = current user's InfluencerProfile
        │   │   ├─ artisan = selected ArtisanProfile
        │   │   ├─ status = 'pending'
        │   │   └─ Save to database
        │   │
        │   └─> Show success message
        │       └─> Redirect to collaborations_list
        │
        └─> Artisan can later accept/reject in dashboard
            ├─> Accept: status = 'accepted' + response message
            └─> Reject: status = 'rejected' + response message
```

---

## File Structure

```
Capstone_project/
├── templates/
│   ├── base.html                          [MODIFIED - Added Influencers link]
│   ├── influencers/
│   │   ├── influencers_list.html         [CREATED - Browse all influencers]
│   │   └── influencer_detail.html        [CREATED - View influencer profile]
│   │
│   └── collaborations/
│       └── new_request.html              [CREATED - Send collaboration request]
│
├── influencers/
│   ├── models.py                         [InfluencerProfile - Already exists]
│   ├── views.py                          [MODIFIED - Added list & detail views]
│   ├── urls.py                           [CREATED - URL routing]
│   ├── admin.py                          [Already configured]
│   └── migrations/
│       └── 0001_initial.py               [Already exists]
│
├── collaborations/
│   ├── models.py                         [CollaborationRequest - Already exists]
│   ├── views.py                          [Already configured]
│   ├── urls.py                           [Already configured]
│   ├── admin.py                          [Already configured]
│   └── migrations/
│
├── accounts/
│   ├── models.py                         [User model with roles]
│   ├── decorators.py                     [Role-based decorators - Already exists]
│   └── ...
│
├── artisanedge/
│   ├── urls.py                           [MODIFIED - Added influencers URL]
│   └── settings.py
│
└── INFLUENCER_IMPLEMENTATION.md          [CREATED - Detailed documentation]
```

---

## Database Schema

```sql
-- User table (existing)
CREATE TABLE accounts_user (
    id INT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    role VARCHAR(20) CHECK (role IN ('customer', 'artisan', 'influencer', 'admin')),
    created_at TIMESTAMP
);

-- InfluencerProfile table (existing)
CREATE TABLE influencers_profile (
    id INT PRIMARY KEY,
    user_id INT UNIQUE REFERENCES accounts_user(id),
    niche VARCHAR(50),
    bio TEXT,
    instagram_handle VARCHAR(100),
    instagram_followers INT,
    youtube_handle VARCHAR(100),
    youtube_subscribers INT,
    facebook_link VARCHAR(255),
    twitter_handle VARCHAR(100),
    personal_website VARCHAR(255),
    rating DECIMAL(3,2),
    total_collaborations INT,
    collaboration_rate DECIMAL(5,2),
    is_verified BOOLEAN,
    is_featured BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- ArtisanProfile table (existing)
CREATE TABLE artisans_profile (
    id INT PRIMARY KEY,
    user_id INT UNIQUE REFERENCES accounts_user(id),
    craft_type VARCHAR(50),
    description TEXT,
    workshop_location VARCHAR(255),
    rating DECIMAL(3,2),
    total_products INT,
    total_sales INT,
    is_featured BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- CollaborationRequest table (existing)
CREATE TABLE collaborations_request (
    id INT PRIMARY KEY,
    influencer_id INT REFERENCES influencers_profile(id),
    artisan_id INT REFERENCES artisans_profile(id),
    title VARCHAR(255),
    description TEXT,
    proposed_terms TEXT,
    commission_percentage DECIMAL(5,2),
    flat_rate DECIMAL(10,2),
    status VARCHAR(20) CHECK (status IN ('pending', 'accepted', 'rejected', 'cancelled')),
    requested_at TIMESTAMP,
    responded_at TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    UNIQUE (influencer_id, artisan_id)  -- Prevent duplicate requests
);
```

---

## URL Routing Map

```
/
├── influencers/
│   ├── (GET)              → influencers:list        (public)
│   └── <id>/              → influencers:detail      (public)
│       (GET)
│
└── collaborations/
    └── request/
        ├── new/           → new_collab_request     (influencer-only)
        │   (GET, POST)
        │
        └── <id>/
            ├── accept/    → accept_collab          (artisan-only)
            │   (GET)
            │
            └── reject/    → reject_collab          (artisan-only)
                (GET)
```

---

## Security & Validation

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY MEASURES                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ 1. CSRF Protection                                                │
│    └─ All forms use {% csrf_token %}                             │
│                                                                   │
│ 2. Authentication                                                 │
│    └─ @login_required decorator on sensitive views               │
│                                                                   │
│ 3. Authorization (Role-Based)                                    │
│    ├─ @influencer_required → Only influencers                    │
│    ├─ @artisan_required → Only artisans                          │
│    └─ Role checks in views                                       │
│                                                                   │
│ 4. Data Integrity                                                 │
│    ├─ Unique constraint: (influencer, artisan)                   │
│    │  Prevents duplicate collaboration requests                  │
│    │                                                              │
│    └─ Foreign Key constraints                                    │
│       Ensure referential integrity                               │
│                                                                   │
│ 5. Input Validation                                               │
│    ├─ Form validation in templates                               │
│    ├─ Model validation in views                                  │
│    └─ Django ORM prevents SQL injection                          │
│                                                                   │
│ 6. Error Handling                                                 │
│    ├─ 404.html for non-existent resources                        │
│    ├─ User-friendly error messages                               │
│    └─ Proper HTTP status codes                                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Performance Considerations

```
Optimization Strategies:
├─ Database Queries
│  ├─ Use select_related() for FK relationships
│  ├─ Use prefetch_related() for reverse relations
│  └─ Add database indexes on frequently filtered fields
│
├─ Caching
│  ├─ Cache influencer list (changes less frequently)
│  ├─ Cache collaboration status checks
│  └─ Use memcached or Redis for session data
│
├─ API Pagination
│  ├─ Paginate influencer list (50 per page)
│  ├─ Lazy load collaborations
│  └─ Implement infinite scroll (optional)
│
└─ Frontend
   ├─ Minify CSS/JS
   ├─ Compress images
   ├─ Use CDN for static files
   └─ Implement lazy loading for images
```

---

This architecture ensures:
✅ Clear separation of concerns
✅ Role-based security
✅ Scalability
✅ Maintainability
✅ User-friendly experience
