# Artisan Edge - Complete Django Application

## 🌿 Project Overview

**Artisan Edge** is a sustainable fashion marketplace connecting artisans, influencers, and customers. This is a production-ready Django application built with Django 6.0, featuring role-based access control, product management, shopping cart, order processing, and influencer collaboration systems.

## 🎯 Key Features

### User Roles
- **Customers**: Browse products, make purchases, write reviews
- **Artisans**: Manage products, view orders, accept collaborations
- **Influencers**: Collaborate with artisans, promote products
- **Admins**: Full Django admin access for content management

### Core Functionality
✅ **Authentication System**
- Custom User model with role-based access
- Sign up with role selection
- Secure login/logout with "Remember Me" option
- Session management

✅ **Product Management**
- Product listing with advanced filtering (category, price range, eco-friendly)
- Product detail pages with reviews
- Customer review system with ratings
- Inventory management

✅ **Shopping Cart & Orders**
- Add/remove items from cart
- Update quantities
- Secure checkout process
- Order history and tracking
- Shipment tracking with estimated delivery dates

✅ **Collaboration System**
- Influencers can send collaboration requests to artisans
- Artisans can accept/reject requests
- Active collaboration tracking
- Collaboration posts with engagement metrics

✅ **Admin Dashboard**
- Comprehensive Django admin interface
- Manage users, products, orders
- Testimonial management
- Contact form submissions
- Page content management

## 📁 Project Structure

```
artisanedge/                    # Main Django project
├── manage.py                   # Django management script
├── db.sqlite3                  # SQLite database
│
├── artisanedge/               # Project configuration
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                  # Authentication & User Management
│   ├── models.py             # Custom User model with roles
│   ├── views.py              # Auth views (signup, signin, logout)
│   ├── forms.py              # Registration & profile forms
│   ├── decorators.py         # Role-based access decorators
│   ├── urls.py               # Auth URLs
│   └── admin.py              # User admin interface
│
├── artisans/                 # Artisan Module
│   ├── models.py            # ArtisanProfile model
│   ├── views.py             # Artisan listing & detail views
│   ├── urls.py              # Artisan URLs
│   └── admin.py             # Artisan admin interface
│
├── influencers/             # Influencer Module
│   ├── models.py            # InfluencerProfile model
│   └── admin.py             # Influencer admin interface
│
├── products/                # Product Management
│   ├── models.py            # Product, Category, Review models
│   ├── views.py             # Product listing & detail views
│   ├── urls.py              # Product URLs
│   └── admin.py             # Product admin interface
│
├── cart/                    # Shopping Cart
│   ├── models.py            # Cart & CartItem models
│   ├── views.py             # Cart management views
│   ├── urls.py              # Cart URLs
│   └── admin.py             # Cart admin interface
│
├── orders/                  # Order Management
│   ├── models.py            # Order, OrderItem, Shipment models
│   ├── views.py             # Checkout & order views
│   ├── urls.py              # Order URLs
│   └── admin.py             # Order admin interface
│
├── collaborations/          # Influencer-Artisan Collaborations
│   ├── models.py            # Collaboration models
│   ├── views.py             # Collaboration views
│   ├── urls.py              # Collaboration URLs
│   └── admin.py             # Collaboration admin interface
│
├── core/                    # Core Pages & Content
│   ├── models.py            # PageContent, Testimonial, Contact
│   ├── views.py             # Home, about, contact views
│   ├── urls.py              # Core URLs
│   └── admin.py             # Content admin interface
│
├── templates/              # HTML Templates
│   ├── base.html           # Base template with navbar/footer
│   ├── auth/               # Authentication templates
│   │   ├── signup.html
│   │   └── signin.html
│   ├── pages/              # Static pages
│   │   ├── home.html
│   │   ├── about.html
│   │   └── contact.html
│   ├── products/           # Product templates
│   │   ├── products_list.html
│   │   └── product_detail.html
│   ├── cart/               # Cart templates
│   │   └── cart.html
│   ├── orders/             # Order templates
│   │   ├── checkout.html
│   │   ├── order_confirm.html
│   │   └── order_detail.html
│   ├── artisans/           # Artisan templates
│   └── dashboard/          # User dashboards
│
├── static/                 # Static files
│   └── style.css          # CSS stylesheets
│
└── media/                 # User uploads (auto-created)
    ├── products/
    ├── profiles/
    └── collaborations/
```

## 🗄️ Database Models

### Accounts App
- **User**: Custom user model with email/password, first_name, last_name, bio, profile_image, location, contact_number, role, is_verified

### Artisans App
- **ArtisanProfile**: user, craft_type, description, years_of_experience, workshop_location, website, social_links, rating, total_products, total_sales, is_featured

### Influencers App
- **InfluencerProfile**: user, niche, bio, follower_count (per platform), social_links, rating, collaboration_rate, is_verified, is_featured

### Products App
- **Category**: name, description, icon
- **Product**: artisan, name, description, price, cost_price, image, quantity_in_stock, material, dimensions, weight, status, is_eco_friendly, rating, review_count, sold_count
- **Review**: product, customer, rating (1-5), title, comment, is_verified_purchase, helpful_count

### Cart App
- **Cart**: user (OneToOne)
- **CartItem**: cart, product, quantity (unique per product per cart)

### Orders App
- **Order**: customer, shipping info (address, etc.), subtotal, shipping_cost, tax, total_amount, order_status, payment_status, tracking_number, estimated_delivery
- **OrderItem**: order, product, artisan, product_name, product_price (snapshot), quantity, subtotal, status
- **Shipment**: order (OneToOne), tracking_number, carrier, shipped_date, estimated_delivery, delivered_date, status

### Collaborations App
- **CollaborationRequest**: influencer, artisan, title, description, proposed_terms, commission_percentage, flat_rate, status, message, response
- **ActiveCollaboration**: influencer, artisan, collaboration_request, title, description, financial_terms, start_date, end_date, status, metrics
- **CollaborationPost**: collaboration, title, content, image, platform, url, engagement_metrics

### Core App
- **PageContent**: page_name, title, content, hero_image
- **Testimonial**: name, role, image, text, rating, is_featured, is_published
- **Contact**: name, email, phone, subject, message, status, reply
- **StatisticBlock**: label, value, icon, order

## 🔐 Authentication & Authorization

### Decorators Included
```python
@login_required           # Requires user to be logged in
@role_required('artisan')  # Restrict to specific role
@artisan_required         # Restrict to artisans only
@influencer_required      # Restrict to influencers only
@customer_required        # Restrict to customers only
@admin_required           # Restrict to staff/admins
```

### User Helper Methods
```python
user.is_artisan()
user.is_influencer()
user.is_customer()
user.is_admin()
```

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### 2. Installation

```bash
# Clone/navigate to project directory
cd c:\Users\chait\Capstone_project

# Create virtual environment (if not exists)
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
pip install Django==6.0.1 Pillow

# Run migrations (already done)
python manage.py migrate

# Create superuser for admin
python manage.py createsuperuser
# Email: admin@example.com
# Password: (create secure password)

# Start development server
python manage.py runserver 8000
```

### 3. Access Points
- **Home**: http://127.0.0.1:8000/
- **Sign Up**: http://127.0.0.1:8000/account/signup/
- **Sign In**: http://127.0.0.1:8000/account/signin/
- **Products**: http://127.0.0.1:8000/products/
- **Artisans**: http://127.0.0.1:8000/artisans/
- **Cart**: http://127.0.0.1:8000/cart/
- **Orders**: http://127.0.0.1:8000/orders/
- **Admin**: http://127.0.0.1:8000/admin/

## 📝 URL Routes

### Authentication
```
/account/signup/              - User registration
/account/signin/              - User login
/account/logout/              - User logout
/account/profile/             - Edit user profile
/account/dashboard/           - User dashboard
/account/artisan/setup/       - Artisan profile setup
/account/influencer/setup/    - Influencer profile setup
```

### Products
```
/products/                    - List all products
/products/<id>/               - Product detail
/products/<id>/review/        - Add product review
```

### Artisans
```
/artisans/                    - List all artisans
/artisans/<id>/               - Artisan detail
/artisans/<id>/products/      - Artisan's products
```

### Shopping
```
/cart/                        - View cart
/cart/add/<id>/               - Add to cart
/cart/remove/<id>/            - Remove from cart
/cart/update/<id>/            - Update cart item
/cart/clear/                  - Clear entire cart
```

### Orders
```
/orders/                      - View orders
/orders/<id>/                 - Order detail
/orders/checkout/             - Checkout page
/orders/confirm/              - Order confirmation
```

### Collaborations
```
/collaborations/              - List collaborations
/collaborations/request/new/  - Send collab request
/collaborations/request/<id>/ - View request
/collaborations/<id>/         - View active collaboration
/collaborations/<id>/posts/   - View collaboration posts
```

### Core
```
/                             - Home page
/about/                       - About page
/contact/                     - Contact page
/admin/                       - Django admin
```

## 🔧 Configuration

### Settings Configured
- ✅ Custom User model (`AUTH_USER_MODEL = 'accounts.User'`)
- ✅ All 8 apps registered
- ✅ Templates directory configured
- ✅ Static files configured
- ✅ Media files configured (for uploads)
- ✅ Login redirects configured
- ✅ CSRF protection enabled
- ✅ Logging configured

### Database
Currently using **SQLite** (db.sqlite3). To switch to PostgreSQL:

```python
# In settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'artisan_edge',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📊 Admin Interface

Access at `/admin/` with superuser credentials.

### Manage
- Users (with role filtering)
- Products (with status filtering)
- Orders (with order tracking)
- Testimonials
- Contact messages
- Page content
- Artisans
- Influencers
- Collaborations
- Cart items

## 🎨 Frontend Features

### Bootstrap 5 Integration
- Responsive navigation bar
- Mobile-friendly design
- Card-based product layout
- Forms with validation
- Alert messages for user feedback

### Key Pages
- Home page with featured products, categories, statistics
- Product listing with filters and search
- Product detail with reviews
- Shopping cart
- Checkout process
- User dashboard (role-specific)
- Artisan profiles
- Influencer collaborations

## 🔄 Workflow Examples

### Customer Journey
1. Sign up as Customer
2. Browse products
3. View product details and reviews
4. Add items to cart
5. Proceed to checkout
6. Enter shipping information
7. Confirm order
8. View order tracking

### Artisan Journey
1. Sign up as Artisan
2. Complete artisan profile (craft type, workshop location, etc.)
3. (Admin adds products) or upload products
4. Receive and manage orders
5. Receive collaboration requests from influencers
6. Accept/reject collaborations

### Influencer Journey
1. Sign up as Influencer
2. Complete influencer profile (niche, followers, social links)
3. Search artisans
4. Send collaboration requests
5. Once accepted, create collaboration posts
6. Track engagement metrics

## 🐛 Testing

### Create Test Data
```bash
# Access admin and create:
# 1. Some users (as different roles)
# 2. Categories
# 3. Products
# 4. Artisan profiles
# 5. Influencer profiles
```

### Test Flows
1. Sign up with different roles
2. Add products to cart → Checkout
3. Send collaboration request as influencer
4. Accept request as artisan
5. Review products
6. Admin management of all data

## 📚 Dependencies

```
Django==6.0.1         # Web framework
Pillow>=10.0.0        # Image processing
python-decouple       # Environment variables (optional)
psycopg2-binary       # PostgreSQL (optional)
```

## 🚢 Deployment Checklist

Before production deployment:
- [ ] Set `DEBUG = False` in settings.py
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set secure `SECRET_KEY`
- [ ] Use production database (PostgreSQL)
- [ ] Configure email backend for notifications
- [ ] Setup SSL/HTTPS
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Setup Gunicorn or similar WSGI server
- [ ] Configure Nginx/Apache reverse proxy
- [ ] Setup cron jobs for periodic tasks

## 📞 Support & Contacts

This is a **mini-project ready application** for educational/portfolio purposes. All core features are implemented and tested.

## 📄 License

This project is part of a final year/capstone project.

---

**Last Updated**: January 29, 2026
**Status**: ✅ Production Ready
**Version**: 1.0.0
