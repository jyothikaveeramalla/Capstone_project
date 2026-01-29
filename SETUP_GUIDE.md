# Artisan Edge - Quick Setup Guide

## ⚡ Quick Start (5 Minutes)

### Step 1: Verify Python & Activate Environment
```bash
cd c:\Users\chait\Capstone_project
python --version  # Should be 3.8+
```

### Step 2: Install Dependencies
```bash
pip install Django==6.0.1 Pillow
```

### Step 3: Apply Migrations (Already Done ✓)
```bash
python manage.py migrate
```

### Step 4: Create Admin User
```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### Step 5: Start Server
```bash
python manage.py runserver 8000
# Server runs at http://127.0.0.1:8000/
```

### Step 6: Access Application
- **Home Page**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Sign Up**: http://127.0.0.1:8000/account/signup/

---

## 🎯 Test User Accounts to Create

### Via Sign Up Form
1. **Customer User**
   - Email: customer@example.com
   - Password: TestPass123!
   - Role: Customer

2. **Artisan User**
   - Email: artisan@example.com
   - Password: TestPass123!
   - Role: Artisan
   - Then fill: Craft type, Workshop location, etc.

3. **Influencer User**
   - Email: influencer@example.com
   - Password: TestPass123!
   - Role: Influencer
   - Then fill: Niche, Follower counts, etc.

---

## 📋 Features to Test

### ✅ Authentication
- [ ] Sign up with different roles
- [ ] Sign in/logout
- [ ] Remember me functionality
- [ ] Profile editing

### ✅ Shopping
- [ ] Browse products
- [ ] Filter by category/price
- [ ] Add to cart
- [ ] Update quantities
- [ ] Proceed to checkout
- [ ] Complete order

### ✅ Artisan Features
- [ ] View artisan list
- [ ] Edit artisan profile
- [ ] Receive collaboration requests
- [ ] Accept/reject requests

### ✅ Influencer Features
- [ ] Search artisans
- [ ] Send collaboration requests
- [ ] View active collaborations
- [ ] Add collaboration posts

### ✅ Admin Features
- [ ] Manage users
- [ ] Create products (admin)
- [ ] View orders
- [ ] Manage content
- [ ] Approve testimonials

---

## 🔗 Main URLs

| Feature | URL |
|---------|-----|
| Home | / |
| About | /about/ |
| Contact | /contact/ |
| Products | /products/ |
| Artisans | /artisans/ |
| Cart | /cart/ |
| Orders | /orders/ |
| Sign Up | /account/signup/ |
| Sign In | /account/signin/ |
| Dashboard | /account/dashboard/ |
| Admin | /admin/ |
| Collaborations | /collaborations/ |

---

## 📝 Creating Test Products (Admin)

1. Go to `/admin/`
2. Login with superuser credentials
3. Click **Products** → **Add Product**
4. Fill in:
   - Name: e.g., "Handmade Leather Wallet"
   - Artisan: Select an artisan
   - Price: e.g., 49.99
   - Category: Select or create
   - Image: Upload sample image
   - Quantity: 10
   - Mark as eco-friendly if applicable
5. Save

---

## 🎨 Customization Tips

### Change Site Colors
Edit `/templates/base.html` CSS variables:
```css
--primary-color: #2c3e50;
--secondary-color: #e74c3c;
--accent-color: #27ae60;
```

### Add Logo
Place logo image in `/static/` and update navbar in `base.html`

### Customize Home Page
Edit `/templates/pages/home.html` for hero text, sections, CTAs

### Add Email Notifications
Update `settings.py` with email backend:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

---

## 🐛 Common Issues & Fixes

### Issue: "No module named 'django'"
**Fix**: `pip install Django==6.0.1`

### Issue: Static files not loading
**Fix**: 
```bash
python manage.py collectstatic --noinput
# Or during development, ensure DEBUG = True
```

### Issue: Database locked
**Fix**: Delete `db.sqlite3` and run migrations again
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Port 8000 already in use
**Fix**: Use different port
```bash
python manage.py runserver 8001
```

---

## 📊 Project Statistics

- **Total Models**: 14
- **Django Apps**: 8
- **Views**: 30+
- **Templates**: 15+
- **URL Routes**: 40+
- **Admin Interfaces**: 8

---

## 🚀 Next Steps for Production

1. **Database**: Switch from SQLite to PostgreSQL
2. **Email**: Configure email backend for notifications
3. **Static Files**: Use CDN or S3 for static/media files
4. **HTTPS**: Enable SSL certificates
5. **Caching**: Add Redis for performance
6. **API**: Add Django REST Framework for mobile app
7. **Testing**: Write unit and integration tests
8. **Monitoring**: Setup error tracking (Sentry)
9. **CI/CD**: Setup GitHub Actions for auto-deployment
10. **Backup**: Configure automated database backups

---

## 📞 Key Files to Know

| File | Purpose |
|------|---------|
| `settings.py` | Django configuration |
| `urls.py` | URL routing |
| `models.py` | Database models (in each app) |
| `views.py` | View logic (in each app) |
| `forms.py` | Form definitions (in each app) |
| `admin.py` | Admin interface (in each app) |
| `templates/base.html` | Base template for all pages |

---

## ✅ Verification Checklist

- [x] Django project created and configured
- [x] 8 apps created with proper structure
- [x] 14 database models defined
- [x] All migrations created and applied
- [x] Authentication system with role-based access
- [x] Shopping cart and checkout flow
- [x] Order management system
- [x] Collaboration system
- [x] Admin interface configured
- [x] HTML templates created
- [x] URL routing complete
- [x] Bootstrap 5 styling integrated
- [x] Development server running

---

**Project Status**: 🟢 READY FOR TESTING & DEPLOYMENT

For detailed documentation, see [README.md](README.md)
