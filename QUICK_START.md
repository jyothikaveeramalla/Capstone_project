# 🔐 Authentication Quick Start Guide

## What Was Added

A complete authentication system for your Artisan Edge website using **localStorage** (ready for Django backend integration).

---

## 📁 New Files Created

### Templates
- **`signin.html`** - Sign in page with email/password form
- **`signup.html`** - Sign up page with role selection

### Static Files
- **`auth.js`** - Core authentication module (handles login, signup, session management)

### Documentation
- **`AUTHENTICATION.md`** - Complete technical documentation

---

## 🚀 Quick Test

### 1. **Create New Account**
```
URL: http://localhost:8000/artisanapp/templates/signup.html
- Select Role: Customer (or Artisan/Influencer)
- Name: Your Name
- Email: test@example.com
- Password: password123
- Accept Terms
- Click "Create Account" → Auto-login → Redirects to marketplace
```

### 2. **Test Shopping (Requires Login)**
```
URL: http://localhost:8000/artisanapp/templates/marketplace.html
- Already logged in from signup ✓
- Click "Add to Cart" → Works!
- Click "Checkout" → Shows success message
```

### 3. **Test Logout & Re-login**
```
- Navbar shows: "👤 Your Name (Customer) | Sign Out"
- Click "Sign Out" → Returns to home
- Navbar shows: "Sign In | Sign Up"
- Click "Sign In" → Use email & password from signup
```

### 4. **Test Auth Guard (What Happens Without Login)**
```
1. Open a new private/incognito window
2. Go to marketplace.html
3. Try "Add to Cart" WITHOUT signing in
   → Yellow warning appears: "You need to sign in"
4. Click Sign In link
5. After login → Redirects back to marketplace.html
```

---

## 🔑 Features Checklist

✅ **Sign Up with Role Selection**
- Artisan (for crafts sellers)
- Influencer (for promoters)
- Customer (for shoppers)

✅ **Sign In with Email/Password**
- Session persists on page refresh
- Shows demo account on signin page

✅ **Role-Based User Display**
- Shows logged-in user name and role in navbar
- Different roles can be tracked (not yet implemented in UI)

✅ **Cart Protection**
- Must be logged in to add items
- Must be logged in to checkout
- Shows friendly auth prompt

✅ **Auto-Redirect**
- After login, returns to the page you were trying to access
- Smooth user experience

✅ **Sign Out**
- Clears all session data
- Returns navbar to Sign In/Sign Up links

✅ **Form Validation**
- Email format validation
- Password strength requirements
- Password match validation
- Real-time requirement indicators

---

## 🎯 How It Works (Technical Overview)

### Authentication Flow
```
User Signup → Create Account in Browser
                    ↓
            Auto-Login & Stored in localStorage
                    ↓
            Navbar Updates Automatically
                    ↓
            User can Add to Cart & Checkout
                    ↓
            Click "Sign Out" → Session Cleared
```

### localStorage Keys Used
```
artisanedge_isLoggedIn  → "true" or "false"
artisanedge_user        → {email, fullName, role}
artisanedge_userRole    → "Customer" / "Artisan" / "Influencer"
artisanedge_users       → All registered users
artisanedge_redirectUrl → URL to go to after login
```

---

## 🛡️ Important: This is Demo-Only!

⚠️ **Current State**: Frontend-only with localStorage
- ✗ No password encryption
- ✗ No server validation
- ✗ No database persistence
- ✗ Perfect for testing & development

✅ **Next Steps for Production**:
1. Create Django User model
2. Add API endpoints for auth
3. Replace localStorage with Django sessions
4. Hash passwords with bcrypt
5. Add email verification
6. Implement rate limiting

See `AUTHENTICATION.md` for detailed integration steps.

---

## 📝 Code Examples

### Check if User is Logged In
```javascript
if (auth.isLoggedIn()) {
    console.log("User is logged in!");
    const user = auth.getCurrentUser();
    console.log("Welcome, " + user.fullName);
}
```

### Get User Information
```javascript
const user = auth.getCurrentUser();
// Returns: {email, fullName, role}

const role = auth.getUserRole();
// Returns: "Customer" or "Artisan" or "Influencer"
```

### Require Login for an Action
```javascript
function addToCart() {
    if (!auth.isLoggedIn()) {
        auth.setRedirectUrl(window.location.href);
        window.location.href = 'signin.html';
        return;
    }
    // Add to cart logic here
}
```

### Logout
```javascript
auth.logout();
window.location.href = 'index.html';
```

---

## 🐛 Troubleshooting

### "Add to Cart doesn't work"
- Open browser console (F12)
- Type: `auth.isLoggedIn()`
- Should return `true`
- If `false`, sign in first

### "Can't sign up"
- Check password is at least 6 characters
- Check email format is valid
- Check browser console for errors

### "Logged in but navbar shows Sign In"
- Refresh the page (Ctrl+R)
- navbar initializes on page load

### "Lost login after closing browser"
- This is normal for demo
- In production, Django sessions persist across browser restarts

---

## 📚 File Locations

```
c:\Users\chait\Capstone_project\
├── artisanapp\
│   ├── templates\
│   │   ├── signin.html         ← NEW: Login page
│   │   ├── signup.html         ← NEW: Registration page
│   │   ├── index.html          ← UPDATED: Added auth.js
│   │   ├── marketplace.html    ← UPDATED: Auth guards + checkout
│   │   ├── about.html          ← UPDATED: Added auth.js
│   │   ├── artisans.html       ← UPDATED: Added auth.js
│   │   ├── contact.html        ← UPDATED: Added auth.js
│   │   └── influencers.html    ← UPDATED: Added auth.js
│   └── static\
│       ├── auth.js             ← NEW: Auth system core
│       └── script.js           ← UPDATED: Auth form guards
└── AUTHENTICATION.md           ← NEW: Full documentation
```

---

## ✨ Next Features to Add

1. **User Profile Page**
   - Edit profile information
   - Change password
   - View order history

2. **Role-Specific Features**
   - Artisans: Upload & manage products
   - Influencers: Create campaigns
   - Customers: View wishlists, reviews

3. **Advanced Auth**
   - Password reset via email
   - Two-factor authentication
   - Social login (Google, GitHub)
   - Account verification

4. **Security Features**
   - Login attempt limiting
   - Session timeout
   - Activity logging
   - Admin dashboard

---

## 🤝 Support

For questions or issues:
1. Check `AUTHENTICATION.md` for detailed docs
2. Review `auth.js` code comments
3. Check browser console for error messages
4. Test with demo account first

---

**Ready to test?** Start with the signup page!
