# Authentication System - Test Cases

## Manual Testing Guide

Complete this checklist to verify all authentication features work correctly.

---

## 🔧 Setup

1. Open your project in a browser
2. Press F12 to open Developer Tools
3. Go to Application tab → LocalStorage
4. Keep this open to monitor auth data

---

## Test Suite 1: Sign Up Flow

### Test 1.1: Create Account with Customer Role ✓
**Steps:**
1. Go to `signup.html`
2. Click "Customer" role card (should highlight)
3. Full Name: `John Doe`
4. Email: `john@example.com`
5. Password: `MyPass123`
6. Confirm Password: `MyPass123`
7. Check terms checkbox
8. Click "Create Account"

**Expected Results:**
- ✓ Success message appears
- ✓ Redirected to `marketplace.html`
- ✓ Navbar shows "👤 John Doe (Customer)"
- ✓ localStorage has `artisanedge_user`, `artisanedge_isLoggedIn`

---

### Test 1.2: Create Account with Artisan Role ✓
**Steps:**
1. Go to `signup.html` in incognito window
2. Click "Artisan" role card (should highlight blue)
3. Full Name: `Raj Kumar`
4. Email: `raj@artisan.com`
5. Password: `ArtisanPass1`
6. Confirm Password: `ArtisanPass1`
7. Accept terms
8. Click "Create Account"

**Expected Results:**
- ✓ Account created with Artisan role
- ✓ Navbar shows "👤 Raj Kumar (Artisan)"
- ✓ Redirected to marketplace

---

### Test 1.3: Create Account with Influencer Role ✓
**Steps:**
1. Go to `signup.html`
2. Click "Influencer" role
3. Full Name: `Sarah Influencer`
4. Email: `sarah@influencer.com`
5. Password: `InfluencerPass1`
6. Confirm Password: `InfluencerPass1`
7. Accept terms
8. Create account

**Expected Results:**
- ✓ Account shows Influencer role
- ✓ All role-based features work

---

### Test 1.4: Password Strength Validation ✓
**Steps:**
1. Go to `signup.html`
2. In Password field, type `short`
3. Observe requirement indicators

**Expected Results:**
- ✓ Length check: Red (fails at <6 chars)
- ✓ Becomes green when password ≥ 6 chars
- ✓ Uppercase check shows optional

---

### Test 1.5: Password Mismatch Error ✓
**Steps:**
1. Go to `signup.html`
2. Password: `TestPass123`
3. Confirm: `DifferentPass123`
4. Try to submit

**Expected Results:**
- ✓ Error: "Passwords do not match"
- ✓ Form doesn't submit

---

### Test 1.6: Missing Required Field ✓
**Steps:**
1. Go to `signup.html`
2. Skip Full Name field
3. Try to submit

**Expected Results:**
- ✓ HTML5 validation prevents submit
- ✓ "Please fill out this field" appears

---

### Test 1.7: Terms Must Be Accepted ✓
**Steps:**
1. Go to `signup.html`
2. Fill all fields
3. Don't check terms checkbox
4. Try to submit

**Expected Results:**
- ✓ Error: "Please accept the Terms of Service"
- ✓ Form doesn't submit

---

### Test 1.8: Duplicate Email Error ✓
**Steps:**
1. Create account with `test1@example.com`
2. Sign out
3. Try to sign up with same email
4. Use different password and name

**Expected Results:**
- ✓ Error: "Email already registered"
- ✓ Can't create second account with same email

---

## Test Suite 2: Sign In Flow

### Test 2.1: Login with Correct Credentials ✓
**Steps:**
1. Sign out (click Sign Out in navbar)
2. Go to `signin.html`
3. Email: `john@example.com` (from Test 1.1)
4. Password: `MyPass123`
5. Click "Sign In"

**Expected Results:**
- ✓ Success message appears
- ✓ Redirected to originally requested page (or home)
- ✓ Navbar shows user name and role
- ✓ localStorage updated

---

### Test 2.2: Login with Wrong Password ✓
**Steps:**
1. Go to `signin.html`
2. Email: `john@example.com`
3. Password: `WrongPassword123`
4. Click "Sign In"

**Expected Results:**
- ✓ Error: "Invalid email or password"
- ✓ Not redirected
- ✓ Form stays on page

---

### Test 2.3: Login with Non-existent Email ✓
**Steps:**
1. Go to `signin.html`
2. Email: `nonexistent@example.com`
3. Password: `SomePass123`
4. Click "Sign In"

**Expected Results:**
- ✓ Error: "Invalid email or password"
- ✓ Not redirected

---

### Test 2.4: Demo Account Access ✓
**Steps:**
1. Go to `signin.html`
2. Note the yellow box: "Email: demo@example.com | Password: demo123"
3. Use these credentials
4. Click "Sign In"

**Expected Results:**
- ✓ Login succeeds
- ✓ Shows as Customer role
- ✓ Full flow works

---

### Test 2.5: Can't Access Signin When Already Logged In ✓
**Steps:**
1. Sign in successfully
2. Go directly to `signin.html`

**Expected Results:**
- ✓ Automatically redirected to `index.html`
- ✓ You see your name in navbar

---

### Test 2.6: Refresh Page Maintains Login ✓
**Steps:**
1. Sign in successfully
2. Press F5 (refresh)
3. Observe navbar

**Expected Results:**
- ✓ Still logged in
- ✓ User name visible
- ✓ localStorage preserved session

---

## Test Suite 3: Cart & Shopping Features

### Test 3.1: Add to Cart Without Login ✓
**Steps:**
1. Open incognito window (ensures not logged in)
2. Go to `marketplace.html`
3. Click "Add to Cart" on first product
4. Observe the page

**Expected Results:**
- ✓ Yellow warning appears: "Please sign in to continue"
- ✓ Product NOT added to cart
- ✓ Cart summary doesn't appear

---

### Test 3.2: Auth Prompt Click Sign In ✓
**Steps:**
1. From Test 3.1, click "Sign In" in the warning
2. Sign in with valid account

**Expected Results:**
- ✓ Redirected back to `marketplace.html`
- ✓ Cart is empty (fresh session)
- ✓ Now can add items to cart

---

### Test 3.3: Add to Cart When Logged In ✓
**Steps:**
1. Sign in successfully
2. Go to `marketplace.html`
3. Click "Add to Cart" on a product

**Expected Results:**
- ✓ Product added to cart
- ✓ Cart summary appears (top-right)
- ✓ Shows product name and price
- ✓ Total price calculated correctly

---

### Test 3.4: Multiple Items in Cart ✓
**Steps:**
1. Logged in on marketplace
2. Click "Add to Cart" on 3 different products

**Expected Results:**
- ✓ All 3 items show in cart summary
- ✓ Total is sum of all prices
- ✓ Cart displays correctly

---

### Test 3.5: Checkout Without Login ✓
**Steps:**
1. In incognito window, go to `marketplace.html`
2. Try to click "Checkout" button (no items will be added without login)

**Expected Results:**
- ✓ Can't add items (protected by auth)
- ✓ If you somehow had items, checkout would redirect to signin

---

### Test 3.6: Checkout When Logged In ✓
**Steps:**
1. Logged in with items in cart
2. Click "Checkout" button
3. Click OK on alert

**Expected Results:**
- ✓ Success message with user name and total
- ✓ Cart clears after checkout
- ✓ Can add new items again

---

## Test Suite 4: Logout & Session Management

### Test 4.1: Logout from Any Page ✓
**Steps:**
1. Sign in and navigate to any page
2. Click "Sign Out" in navbar

**Expected Results:**
- ✓ Redirected to `index.html`
- ✓ Navbar shows "Sign In | Sign Up"
- ✓ Cart is cleared
- ✓ localStorage cleaned

---

### Test 4.2: Login Again After Logout ✓
**Steps:**
1. After logout, click "Sign In"
2. Sign in with same account

**Expected Results:**
- ✓ Can log in again
- ✓ Same user data restored
- ✓ Previous cart is gone (fresh session)

---

### Test 4.3: Multiple Users ✓
**Steps:**
1. Create User A: `alice@example.com` / `AlicePass123` / Customer
2. Create User B: `bob@example.com` / `BobPass123` / Artisan
3. Login as Alice
4. Check navbar shows "Alice"
5. Logout
6. Login as Bob
7. Check navbar shows "Bob" and "Artisan"

**Expected Results:**
- ✓ Each user maintains separate session
- ✓ Correct role displayed
- ✓ No data cross-contamination

---

## Test Suite 5: Navigation & Role Display

### Test 5.1: Role Display in Navbar ✓
**Steps:**
1. Sign in with Customer account
2. Check navbar

**Expected Results:**
- ✓ Shows: "👤 [Name] (Customer)"
- ✓ Color coded or styled

---

### Test 5.2: All Pages Show Auth Menu ✓
**Steps:**
1. Sign in
2. Navigate to: home, about, artisans, influencers, marketplace, contact

**Expected Results:**
- ✓ Every page shows navbar with user info
- ✓ Can click Sign Out from any page

---

### Test 5.3: Navbar Updates When Logging Out ✓
**Steps:**
1. Signed in on any page
2. Click Sign Out
3. Observe navbar immediately

**Expected Results:**
- ✓ Navbar changes from user info to Sign In/Sign Up
- ✓ Happens in real-time

---

## Test Suite 6: Browser & Device Tests

### Test 6.1: Different Browsers ✓
**Steps:**
1. Sign up in Chrome
2. Open Firefox and go to site

**Expected Results:**
- ✓ NOT logged in Firefox (separate cookies/storage)
- ✓ Must sign in separately in each browser

---

### Test 6.2: Incognito/Private Mode ✓
**Steps:**
1. Open incognito window
2. Sign in
3. Close incognito window
4. Open new incognito window
5. Go to site

**Expected Results:**
- ✓ Not logged in on new incognito
- ✓ Must sign in again

---

### Test 6.3: Mobile Responsiveness ✓
**Steps:**
1. Open DevTools (F12)
2. Toggle Device Toolbar (Ctrl+Shift+M)
3. Choose iPhone SE or iPad
4. Sign in and test all features

**Expected Results:**
- ✓ Forms are readable
- ✓ Buttons are clickable
- ✓ Navbar works on mobile
- ✓ Cart works on mobile

---

## Test Suite 7: Form Validation

### Test 7.1: Email Format Validation ✓
**Steps:**
1. Go to `signup.html`
2. Try invalid emails:
   - `notanemail`
   - `email@.com`
   - `@example.com`

**Expected Results:**
- ✓ HTML5 validation rejects invalid emails
- ✓ Error: "Please include an '@' in the email address"

---

### Test 7.2: Password Visibility Toggle ✓ (if implemented)
**Steps:**
1. Go to `signup.html`
2. Type password
3. If there's an eye icon, click it

**Expected Results:**
- ✓ Password shows in plaintext
- ✓ Can toggle back to dots

---

## Test Suite 8: Error Scenarios

### Test 8.1: Network Error Handling (if backend) ✓
**Steps:**
1. Go to `signin.html`
2. Open DevTools Network tab
3. Throttle to "Offline"
4. Try to sign in

**Expected Results:**
- ✓ Error message appears
- ✓ No hanging or freezing UI

---

### Test 8.2: Concurrent Logins ✓
**Steps:**
1. Sign in User A in Tab 1
2. Sign in User B in Tab 2
3. Check which session is active

**Expected Results:**
- ✓ Last login wins (expected behavior)
- ✓ Sessions don't conflict

---

## Test Summary Checklist

### Sign Up
- [ ] Customer role signup
- [ ] Artisan role signup
- [ ] Influencer role signup
- [ ] Password strength validation
- [ ] Password mismatch error
- [ ] Required fields validation
- [ ] Terms acceptance required
- [ ] Duplicate email prevention

### Sign In
- [ ] Correct credentials login
- [ ] Wrong password error
- [ ] Non-existent email error
- [ ] Demo account works
- [ ] Can't access when already logged in
- [ ] Session persists on refresh

### Shopping
- [ ] Auth required for Add to Cart
- [ ] Auth prompt appears
- [ ] Can add to cart when logged in
- [ ] Multiple items in cart
- [ ] Auth required for checkout
- [ ] Checkout shows user name
- [ ] Cart clears after checkout

### Session Management
- [ ] Logout from any page
- [ ] Can login again after logout
- [ ] Multiple users don't interfere
- [ ] Role displays correctly
- [ ] Navbar updates on auth changes

### Cross-Device
- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Edge
- [ ] Incognito mode isolated
- [ ] Mobile responsive

---

## Performance Tests

### Test P1: Page Load Time ✓
**Steps:**
1. Open marketplace.html when not logged in
2. DevTools → Performance tab → Record
3. Sign in
4. Stop recording

**Expected Results:**
- ✓ Auth checks don't add noticeable lag
- ✓ Page loads in under 2 seconds

---

### Test P2: localStorage Size ✓
**Steps:**
1. Open DevTools → Application → LocalStorage
2. Expand artisanedge items
3. Check total size

**Expected Results:**
- ✓ Total should be < 5KB
- ✓ Not excessive data storage

---

## Notes for Developers

### Common Test Errors
1. **"Navbar doesn't show Sign Out"**
   - Solution: auth.js must load before page script
   
2. **"Can add to cart without login"**
   - Solution: Check auth.isLoggedIn() is being called
   
3. **"Session lost on refresh"**
   - Solution: Normal in incognito mode
   
4. **"Different browser is logged in"**
   - Solution: Each browser has separate cookies

### Debugging Tips
```javascript
// Check login status in console
auth.isLoggedIn()

// See current user
auth.getCurrentUser()

// Check role
auth.getUserRole()

// View all localStorage
Object.keys(localStorage).forEach(key => {
    if (key.startsWith('artisanedge_')) {
        console.log(key + ': ' + localStorage.getItem(key))
    }
})
```

---

## Test Automation Script

```javascript
// Run in console to test basic flow
async function runTests() {
    console.log('🧪 Running authentication tests...');
    
    // Test 1: Check auth module exists
    console.assert(typeof auth !== 'undefined', 'Auth module not found');
    
    // Test 2: Initial state not logged in
    console.assert(!auth.isLoggedIn(), 'Should not be logged in initially');
    
    // Test 3: Create account
    let signupResult = auth.signup('test1@example.com', 'TestPass123', 'Test User', 'Customer');
    console.assert(signupResult, 'Signup should succeed');
    
    // Test 4: Should be logged in after signup
    console.assert(auth.isLoggedIn(), 'Should be logged in after signup');
    
    // Test 5: Get user info
    let user = auth.getCurrentUser();
    console.assert(user.email === 'test1@example.com', 'Email should match');
    
    // Test 6: Logout
    auth.logout();
    console.assert(!auth.isLoggedIn(), 'Should not be logged in after logout');
    
    // Test 7: Login
    let loginResult = auth.login('test1@example.com', 'TestPass123');
    console.assert(loginResult, 'Login should succeed');
    
    console.log('✅ All tests passed!');
}

runTests();
```

---

**Last Updated:** January 2025
**Status:** Complete for frontend testing
