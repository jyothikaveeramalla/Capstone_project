from django.db import models
from accounts.models import User
from artisans.models import ArtisanProfile
from django.core.validators import MinValueValidator

class Category(models.Model):
    """
    Product categories
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)  # For emoji or icon class
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'products_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Product model for items sold by artisans
    """
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('discontinued', 'Discontinued'),
    )
    
    artisan = models.ForeignKey(ArtisanProfile, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # For admin tracking
    
    # Inventory
    quantity_in_stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Media
    image = models.ImageField(upload_to='products/', help_text='Main product image')
    images = models.ImageField(upload_to='products/', blank=True, null=True)  # Multiple images could be JSON
    
    # Details
    dimensions = models.CharField(max_length=100, blank=True, null=True)  # e.g., "20x10x5 cm"
    material = models.CharField(max_length=100, blank=True, null=True)
    weight = models.CharField(max_length=50, blank=True, null=True)  # e.g., "500g"
    
    # Metrics
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    review_count = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)
    
    # Sustainability
    is_eco_friendly = models.BooleanField(default=True)
    sustainability_notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products_product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['artisan', 'status']),
            models.Index(fields=['category']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} by {self.artisan.user.get_full_name()}"
    
    def in_stock(self):
        return self.quantity_in_stock > 0
    
    def discount_percentage(self):
        """Calculate discount if cost_price exists"""
        if self.cost_price and self.cost_price < self.price:
            return int(((self.price - self.cost_price) / self.price) * 100)
        return 0


class Review(models.Model):
    """
    Product reviews from customers
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'products_review'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ['product', 'customer']  # One review per customer per product
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review for {self.product.name} by {self.customer.get_full_name()}"
