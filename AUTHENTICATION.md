# Authentication System Implementation

## Overview

A complete authentication flow has been implemented for the Artisan Edge website using localStorage. Users must sign in or create an account before accessing cart and checkout features.

## Features Implemented

### ✅ Authentication System (`auth.js`)
- **Sign Up**: Users can create accounts with role selection (Artisan, Influencer, Customer)
- **Sign In**: Login with email and password
- **Sign Out**: Logout and clear session
- **Role-Based Access**: Support for three user roles
- **Session Persistence**: Uses localStorage to maintain login state across page refreshes
- **Redirect Management**: Remembers the original page to redirect after login

### ✅ User Interface
1. **Sign In Page** (`signin.html`)
   - Email/password login form
   - Demo account information for testing
   - Link to sign up page
   - Redirect to originally requested page after login

2. **Sign Up Page** (`signup.html`)
   - Interactive role selection (Artisan, Influencer, Customer)
   - Full name, email, password input
   - Password strength requirements display
   - Terms acceptance checkbox
   - Auto-login after successful signup

3. **Navigation Updates**
   - Auth menu shows in navbar with user info when logged in
   - Sign In/Sign Up links when not authenticated
   - Sign Out option for logged-in users
   - User role badge displayed next to name

4. **Cart & Checkout Protection** (marketplace.html)
   - "Add to Cart" button requires authentication
   - Checkout requires authentication
   - Non-authenticated users see auth prompt
   - Automatic redirect to signin.html on unauthorized cart access

## File Structure

```
artisanapp/
├── static/
│   ├── auth.js           # Core authentication module
│   ├── script.js         # Updated with auth guards
│   └── styles.css        # (Existing styles)
├── templates/
│   ├── signin.html       # Sign in page
│   ├── signup.html       # Sign up page
│   ├── index.html        # Updated with auth.js
│   ├── marketplace.html  # Updated with auth guards
│   ├── about.html        # Updated with auth.js
│   ├── artisans.html     # Updated with auth.js
│   ├── contact.html      # Updated with auth.js
│   └── influencers.html  # Updated with auth.js
```

## How to Use

### For Demo/Testing

1. **Create a new account**:
   - Go to `signup.html`
   - Select a role (Artisan, Influencer, or Customer)
   - Fill in details
   - Click "Create Account"

2. **Demo Account** (pre-filled on signin.html):
   - Email: `demo@example.com`
   - Password: `demo123`
   - Role: `Customer`

3. **Shopping Flow**:
   - Sign in or create account
   - Navigate to Marketplace
   - Add items to cart (requires login)
   - Click "Checkout" to place order
   - Sign out when done

### API Reference (`auth.js`)

```javascript
// Check if user is logged in
auth.isLoggedIn() → boolean

// Get current user data
auth.getCurrentUser() → {email, fullName, role}

// Get user role
auth.getUserRole() → string (Artisan, Influencer, Customer)

// Login
auth.login(email, password) → boolean

// Signup
auth.signup(email, password, fullName, role) → boolean

// Logout
auth.logout()

// Check specific role
auth.hasRole(role) → boolean

// Require login (redirects to signin if not authenticated)
auth.requireLogin(currentPageUrl)

// Store URL for redirect after login
auth.setRedirectUrl(url)

// Get and clear redirect URL
auth.getRedirectUrl() → string
```

## LocalStorage Keys

The system uses these localStorage keys (prefixed with `artisanedge_`):

```
- artisanedge_isLoggedIn    : Boolean flag for login status
- artisanedge_user          : JSON string with {email, fullName, role}
- artisanedge_userRole      : String with current user role
- artisanedge_redirectUrl   : String with URL to redirect to after login
- artisanedge_users         : JSON object storing all user accounts
```

## Authentication Flow

```
┌─────────────────────────────────────────────────────┐
│                    User Actions                      │
└─────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
    First Visit?    Shopping?      Direct Visit
         │               │               │
    ┌────┴─────┐  ┌──────┴──────┐  ┌────┴─────┐
    │           │  │             │  │           │
   View          Browse      Add to Cart   Go to Cart
   Content      Products      Checkout       
    │           │             │              │
    ✓ Allowed   │             │              │
               │              │              │
               ▼              ▼              ▼
         Check if         Check if      Check if
         Logged In?       Logged In?     Logged In?
         │                │              │
        No              No             No
         │                │              │
         ▼                ▼              ▼
    Show Auth          Show Auth       Redirect
    Prompt            Prompt          to SignIn
    (Can dismiss)   (Required)        (Forced)
         │                │              │
         ▼                ▼              ▼
    Continue        Redirect         SignIn/
    Browsing        to SignIn        SignUp
                                      │
                                      ▼
                                   Login
                                      │
                                      ▼
                                   Redirect
                                   to Original
                                   Page
```

## Integration with Django Backend

When ready to integrate with Django:

1. **Replace localStorage with server session** in `auth.js`:
   ```javascript
   // Current: localStorage-based
   // Future: CSRF-protected Django session cookies
   ```

2. **Update signup/login methods**:
   ```javascript
   // Current: Client-side validation only
   // Future: POST to /api/auth/signup and /api/auth/login endpoints
   ```

3. **Backend validation**:
   - Password hashing (bcrypt/Argon2)
   - Rate limiting on login attempts
   - JWT or session-based authentication
   - Database persistence for users

4. **Create Django views**:
   ```python
   # In artisanedge/urls.py
   path('api/auth/signup/', SignUpView.as_view()),
   path('api/auth/login/', LoginView.as_view()),
   path('api/auth/logout/', LogoutView.as_view()),
   path('api/auth/me/', CurrentUserView.as_view()),
   ```

5. **Update auth.js** to call these endpoints instead of using localStorage

## Security Notes

### Current State (Demo)
⚠️ **This is a frontend-only implementation for demonstration**
- Passwords are stored in localStorage (NEVER do this in production)
- No encryption or hashing
- Client-side validation only
- No rate limiting

### Production Requirements
- ✅ Use HTTPS only
- ✅ Hash passwords with bcrypt/Argon2
- ✅ Implement CSRF protection
- ✅ Use secure session management (HttpOnly cookies)
- ✅ Add rate limiting on auth endpoints
- ✅ Implement password reset functionality
- ✅ Use JWT with refresh tokens if using token-based auth
- ✅ Validate all inputs server-side
- ✅ Add email verification for new accounts

## Testing Checklist

- [ ] User can sign up with different roles
- [ ] User can sign in with valid credentials
- [ ] Invalid credentials show error message
- [ ] Navbar shows user info when logged in
- [ ] Navbar shows Sign In/Sign Up links when logged out
- [ ] Sign Out clears session
- [ ] Cannot add to cart without authentication
- [ ] Cannot checkout without authentication
- [ ] Auth prompt appears when trying cart actions without login
- [ ] Redirect to signin.html works correctly
- [ ] After login, user is redirected to original page
- [ ] Page refresh maintains login state
- [ ] Already logged in users cannot access signin/signup pages
- [ ] Password requirements are validated on signup
- [ ] Role selection is required on signup
- [ ] Demo account works for quick testing

## Code Examples

### Protecting a Form
```html
<form class="requires-auth" onsubmit="handleSubmit(event)">
    <!-- Form fields -->
</form>

<script>
function handleSubmit(event) {
    if (!auth.isLoggedIn()) {
        auth.setRedirectUrl(window.location.href);
        window.location.href = 'signin.html';
        return;
    }
    // Process form
}
</script>
```

### Checking User Role
```javascript
if (auth.hasRole('Artisan')) {
    // Show artisan-specific features
}

const user = auth.getCurrentUser();
console.log(`Logged in as: ${user.fullName} (${user.email})`);
```

### Initializing Auth on Page Load
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Auto-initialized by auth.js
    // Navbar is automatically updated with auth menu
    
    if (auth.isLoggedIn()) {
        const user = auth.getCurrentUser();
        console.log('Welcome back, ' + user.fullName);
    }
});
```

## Troubleshooting

**Q: Sign In/Sign Up page not working**
- A: Make sure `auth.js` is loaded before the page script. Check browser console for errors.

**Q: Can't add to cart even when logged in**
- A: Verify auth.isLoggedIn() returns true in browser console. Check localStorage for `artisanedge_isLoggedIn`.

**Q: Session clears on page refresh**
- A: This is expected behavior if using incognito mode. localStorage doesn't persist in incognito.

**Q: Created account but can't login**
- A: Check browser console for any error messages. Verify email format is correct.

**Q: Demo account not working**
- A: Try creating a new account instead. Demo account is a suggestion, not automatically created.

## Next Steps

1. Design database schema for users and roles
2. Create Django models for User with role selection
3. Implement JWT authentication or session-based auth
4. Add email verification for new accounts
5. Implement password reset flow
6. Add social login (Google, GitHub)
7. Implement two-factor authentication
8. Add user profile page
9. Implement role-specific features
10. Add audit logging for security events

---

**Documentation Last Updated**: January 2025
**Version**: 1.0 (Frontend Only - localStorage based)
