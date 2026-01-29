# Django Integration Guide

## Migrating from localStorage to Django Backend

This guide shows how to integrate the current frontend authentication system with Django.

---

## Step 1: Create Django User Model

### Update `artisanapp/models.py`

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    ARTISAN = 'Artisan', 'Artisan'
    INFLUENCER = 'Influencer', 'Influencer'
    CUSTOMER = 'Customer', 'Customer'

class CustomUser(AbstractUser):
    """Extended user model with role-based access"""
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'auth_user'  # Use Django's default table name
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
```

### Update `artisanedge/settings.py`

```python
AUTH_USER_MODEL = 'artisanapp.CustomUser'

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_SECURE = True  # Only HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JS access
CSRF_COOKIE_SECURE = True  # Only HTTPS

# CORS for API
INSTALLED_APPS = [
    # ... existing apps
    'corsheaders',
    'rest_framework',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... other middleware
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:3000",
]
```

---

## Step 2: Create Authentication Views

### Create `artisanapp/serializers.py`

```python
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'password', 'password_confirm', 'role']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],  # Use email as username
            first_name=validated_data['first_name'],
            password=validated_data['password'],
            role=validated_data.get('role', 'Customer')
        )
        return user

class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}
```

### Create `artisanapp/views.py`

```python
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import login, logout
from .serializers import SignUpSerializer, SignInSerializer, UserSerializer
from .models import CustomUser

class SignUpView(views.APIView):
    """Register a new user"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # Auto-login after signup
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(views.APIView):
    """Login user"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignOutView(views.APIView):
    """Logout user"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(
            {'message': 'Logged out successfully'},
            status=status.HTTP_200_OK
        )

class CurrentUserView(views.APIView):
    """Get current user info"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            UserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )
```

---

## Step 3: Update URL Configuration

### Update `artisanedge/urls.py`

```python
from django.contrib import admin
from django.urls import path, include
from artisanapp.views import (
    SignUpView, SignInView, SignOutView, CurrentUserView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/signup/', SignUpView.as_view(), name='signup'),
    path('api/auth/signin/', SignInView.as_view(), name='signin'),
    path('api/auth/signout/', SignOutView.as_view(), name='signout'),
    path('api/auth/me/', CurrentUserView.as_view(), name='current_user'),
    # ... other paths
]
```

---

## Step 4: Update Frontend auth.js

### Modified `auth.js` with Backend Integration

```javascript
class AuthSystem {
    constructor() {
        this.apiBase = '/api/auth';
        this.storageKeyPrefix = 'artisanedge_';
    }

    /**
     * Sign up - calls Django backend
     */
    async signup(email, password, fullName, role) {
        try {
            const response = await fetch(`${this.apiBase}/signup/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken'),
                },
                credentials: 'include',
                body: JSON.stringify({
                    email,
                    password,
                    password_confirm: password,
                    first_name: fullName.split(' ')[0],
                    last_name: fullName.split(' ').slice(1).join(' '),
                    role
                })
            });

            if (response.ok) {
                const user = await response.json();
                localStorage.setItem(this.storageKeyPrefix + 'user', JSON.stringify(user));
                return true;
            } else {
                const errors = await response.json();
                this.showError(JSON.stringify(errors));
                return false;
            }
        } catch (error) {
            this.showError('Signup failed: ' + error.message);
            return false;
        }
    }

    /**
     * Sign in - calls Django backend
     */
    async login(email, password) {
        try {
            const response = await fetch(`${this.apiBase}/signin/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCookie('csrftoken'),
                },
                credentials: 'include',
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const user = await response.json();
                localStorage.setItem(this.storageKeyPrefix + 'user', JSON.stringify(user));
                localStorage.setItem(this.storageKeyPrefix + 'userRole', user.role);
                localStorage.setItem(this.storageKeyPrefix + 'isLoggedIn', 'true');
                return true;
            } else {
                this.showError('Invalid email or password');
                return false;
            }
        } catch (error) {
            this.showError('Login failed: ' + error.message);
            return false;
        }
    }

    /**
     * Sign out - calls Django backend
     */
    async logout() {
        try {
            await fetch(`${this.apiBase}/signout/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken'),
                },
                credentials: 'include'
            });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            // Clear local storage
            localStorage.removeItem(this.storageKeyPrefix + 'isLoggedIn');
            localStorage.removeItem(this.storageKeyPrefix + 'user');
            localStorage.removeItem(this.storageKeyPrefix + 'userRole');
        }
    }

    /**
     * Check authentication on page load
     */
    async checkAuth() {
        try {
            const response = await fetch(`${this.apiBase}/me/`, {
                credentials: 'include'
            });

            if (response.ok) {
                const user = await response.json();
                localStorage.setItem(this.storageKeyPrefix + 'user', JSON.stringify(user));
                localStorage.setItem(this.storageKeyPrefix + 'userRole', user.role);
                localStorage.setItem(this.storageKeyPrefix + 'isLoggedIn', 'true');
                return true;
            } else {
                // Not authenticated
                return false;
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            return false;
        }
    }

    /**
     * Get CSRF token from cookie
     */
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // ... rest of the methods remain the same
}

// Check authentication on page load
const auth = new AuthSystem();
document.addEventListener('DOMContentLoaded', async function() {
    await auth.checkAuth();
    auth.initializeAuthUI();
});
```

---

## Step 5: Protect Views with Django

### Protect Cart/Order Views

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """Add item to cart - requires authentication"""
    # User is guaranteed to be authenticated here
    user = request.user
    # Process cart logic
    return Response({'status': 'added'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    """Create order - requires authentication"""
    user = request.user
    # Create order and charge payment
    return Response({'order_id': 123})
```

---

## Step 6: Create Database Migrations

```bash
python manage.py makemigrations artisanapp
python manage.py migrate
```

---

## Benefits of Django Integration

✅ **Security**
- Passwords hashed with PBKDF2
- CSRF protection
- Secure session management
- Server-side validation

✅ **Persistence**
- User data stored in database
- Sessions survive server restarts
- Order history tracking
- User preferences

✅ **Scalability**
- Support multiple servers
- Redis-based sessions
- Database replication
- Performance optimization

✅ **Features**
- Email verification
- Password reset
- Two-factor authentication
- Admin dashboard
- Analytics

---

## Testing the Integration

### Create Test User

```python
from artisanapp.models import CustomUser

user = CustomUser.objects.create_user(
    email='test@example.com',
    username='test@example.com',
    password='testpass123',
    first_name='Test',
    last_name='User',
    role='Customer'
)
```

### Test API Endpoints

```bash
# Sign up
curl -X POST http://localhost:8000/api/auth/signup/ \
  -H "Content-Type: application/json" \
  -d '{"email":"new@example.com","password":"pass123","password_confirm":"pass123","first_name":"John","last_name":"Doe","role":"Customer"}'

# Sign in
curl -X POST http://localhost:8000/api/auth/signin/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Get current user (requires authentication)
curl -X GET http://localhost:8000/api/auth/me/ \
  --cookie "sessionid=YOUR_SESSION_ID"

# Sign out
curl -X POST http://localhost:8000/api/auth/signout/ \
  --cookie "sessionid=YOUR_SESSION_ID"
```

---

## Common Issues & Solutions

### Issue: CSRF Token Missing
**Solution**: Django automatically handles CSRF if using `credentials: 'include'` in fetch

### Issue: Cors errors
**Solution**: Install django-cors-headers and configure CORS_ALLOWED_ORIGINS

### Issue: Session not persisting
**Solution**: Use Django's default SessionBackend or Redis backend

### Issue: Passwords not hashing
**Solution**: Always use `create_user()` method, not `create()`

---

## Next Steps

1. ✅ Replace localStorage with Django sessions
2. ✅ Add email verification
3. ✅ Implement password reset
4. ✅ Add two-factor authentication
5. ✅ Create user profile API
6. ✅ Add role-based permissions
7. ✅ Implement audit logging
8. ✅ Add rate limiting

---

**Ready to integrate?** Start with Step 1: Creating the Django User Model!
