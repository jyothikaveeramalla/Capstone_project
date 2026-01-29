from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator

class User(AbstractUser):
    """
    Custom user model with role-based access control
    """
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('artisan', 'Artisan'),
        ('influencer', 'Influencer'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    bio = models.TextField(blank=True, null=True, max_length=500)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def is_artisan(self):
        return self.role == 'artisan'
    
    def is_influencer(self):
        return self.role == 'influencer'
    
    def is_customer(self):
        return self.role == 'customer'
    
    def is_admin(self):
        return self.role == 'admin' or self.is_staff
