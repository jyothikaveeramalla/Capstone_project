/**
 * Authentication System
 * Handles user login, signup, logout, and role management
 * Uses localStorage for session persistence (ready for Django backend integration)
 */

class AuthSystem {
    constructor() {
        this.storageKeyPrefix = 'artisanedge_';
        this.userKey = `${this.storageKeyPrefix}user`;
        this.isLoggedInKey = `${this.storageKeyPrefix}isLoggedIn`;
        this.userRoleKey = `${this.storageKeyPrefix}userRole`;
        this.redirectUrlKey = `${this.storageKeyPrefix}redirectUrl`;
    }

    /**
     * Sign up new user
     * @param {string} email - User email
     * @param {string} password - User password
     * @param {string} fullName - User's full name
     * @param {string} role - User role (Artisan, Influencer, Customer)
     * @returns {boolean} - Success status
     */
    signup(email, password, fullName, role) {
        if (!email || !password || !fullName || !role) {
            this.showError('All fields are required');
            return false;
        }

        if (!this.validateEmail(email)) {
            this.showError('Invalid email format');
            return false;
        }

        if (password.length < 6) {
            this.showError('Password must be at least 6 characters');
            return false;
        }

        // Check if user already exists (for demo purposes)
        const existingUsers = JSON.parse(localStorage.getItem(`${this.storageKeyPrefix}users`) || '{}');
        if (existingUsers[email]) {
            this.showError('Email already registered');
            return false;
        }

        // Store user (in production, this would be sent to backend)
        const newUser = {
            email,
            password, // In production, NEVER store plain passwords
            fullName,
            role,
            createdAt: new Date().toISOString()
        };

        existingUsers[email] = newUser;
        localStorage.setItem(`${this.storageKeyPrefix}users`, JSON.stringify(existingUsers));

        // Auto-login after signup
        return this.login(email, password);
    }

    /**
     * Login user
     * @param {string} email - User email
     * @param {string} password - User password
     * @returns {boolean} - Success status
     */
    login(email, password) {
        if (!email || !password) {
            this.showError('Email and password are required');
            return false;
        }

        // Retrieve user from storage
        const users = JSON.parse(localStorage.getItem(`${this.storageKeyPrefix}users`) || '{}');
        const user = users[email];

        if (!user || user.password !== password) {
            this.showError('Invalid email or password');
            return false;
        }

        // Store authentication state
        localStorage.setItem(this.isLoggedInKey, 'true');
        localStorage.setItem(this.userKey, JSON.stringify({
            email: user.email,
            fullName: user.fullName,
            role: user.role
        }));
        localStorage.setItem(this.userRoleKey, user.role);

        return true;
    }

    /**
     * Logout user
     */
    logout() {
        localStorage.removeItem(this.isLoggedInKey);
        localStorage.removeItem(this.userKey);
        localStorage.removeItem(this.userRoleKey);
        localStorage.removeItem(this.redirectUrlKey);
    }

    /**
     * Check if user is logged in
     * @returns {boolean} - Login status
     */
    isLoggedIn() {
        return localStorage.getItem(this.isLoggedInKey) === 'true';
    }

    /**
     * Get current user data
     * @returns {Object|null} - User object or null if not logged in
     */
    getCurrentUser() {
        if (!this.isLoggedIn()) return null;
        return JSON.parse(localStorage.getItem(this.userKey) || 'null');
    }

    /**
     * Get current user role
     * @returns {string|null} - User role or null if not logged in
     */
    getUserRole() {
        if (!this.isLoggedIn()) return null;
        return localStorage.getItem(this.userRoleKey);
    }

    /**
     * Check if user is a specific role
     * @param {string} role - Role to check (Artisan, Influencer, Customer)
     * @returns {boolean}
     */
    hasRole(role) {
        return this.getUserRole() === role;
    }

    /**
     * Store the URL to redirect to after login
     * @param {string} url - URL to redirect to
     */
    setRedirectUrl(url) {
        localStorage.setItem(this.redirectUrlKey, url);
    }

    /**
     * Get and clear the redirect URL
     * @returns {string|null} - URL to redirect to
     */
    getRedirectUrl() {
        const url = localStorage.getItem(this.redirectUrlKey);
        localStorage.removeItem(this.redirectUrlKey);
        return url;
    }

    /**
     * Validate email format
     * @param {string} email - Email to validate
     * @returns {boolean}
     */
    validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Show error message (can be enhanced with toast notifications)
     * @param {string} message - Error message
     */
    showError(message) {
        console.error('Auth Error:', message);
        // In production, use a toast notification library
        alert(message);
    }

    /**
     * Show success message
     * @param {string} message - Success message
     */
    showSuccess(message) {
        console.log('Auth Success:', message);
        // In production, use a toast notification library
        alert(message);
    }

    /**
     * Require authentication - redirect to signin if not logged in
     * @param {string} currentPageUrl - Current page URL for redirect after login
     * @returns {boolean} - True if logged in, false otherwise (redirects to signin)
     */
    requireLogin(currentPageUrl = window.location.href) {
        if (!this.isLoggedIn()) {
            this.setRedirectUrl(currentPageUrl);
            window.location.href = 'signin.html';
            return false;
        }
        return true;
    }

    /**
     * Initialize authentication UI
     * Updates navbar with login/logout links based on authentication state
     */
    initializeAuthUI() {
        const navMenu = document.querySelector('.nav-menu');
        if (!navMenu) return;

        // Find or create auth menu
        let authMenu = document.querySelector('.auth-menu');
        if (!authMenu) {
            authMenu = document.createElement('div');
            authMenu.className = 'auth-menu';
            authMenu.style.cssText = `
                display: flex;
                gap: 1rem;
                align-items: center;
                list-style: none;
                margin: 0;
                padding: 0;
            `;
            navMenu.parentElement.appendChild(authMenu);
        }

        if (this.isLoggedIn()) {
            const user = this.getCurrentUser();
            const role = this.getUserRole();
            authMenu.innerHTML = `
                <li style="color: #4a8f4e; font-weight: 600;">
                    👤 ${user.fullName} <span style="font-size: 0.9rem; color: #97d69b;">(${role})</span>
                </li>
                <li><a href="#" onclick="auth.logout(); window.location.href='index.html';" style="color: white; text-decoration: none; cursor: pointer;">Sign Out</a></li>
            `;
        } else {
            authMenu.innerHTML = `
                <li><a href="signin.html">Sign In</a></li>
                <li><a href="signup.html">Sign Up</a></li>
            `;
        }
    }
}

// Initialize global auth object
const auth = new AuthSystem();

// Initialize auth UI on page load
document.addEventListener('DOMContentLoaded', function() {
    auth.initializeAuthUI();
});

// Prevent accessing auth pages if already logged in
function redirectIfLoggedIn() {
    if (auth.isLoggedIn()) {
        window.location.href = 'index.html';
    }
}

// Call on signin/signup page load
document.addEventListener('DOMContentLoaded', function() {
    const currentFile = window.location.pathname.split('/').pop();
    if ((currentFile === 'signin.html' || currentFile === 'signup.html') && auth.isLoggedIn()) {
        redirectIfLoggedIn();
    }
});
