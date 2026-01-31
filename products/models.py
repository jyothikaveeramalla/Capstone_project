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
    team = models.ForeignKey('artisans.ArtisanTeam', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # For admin tracking
    # Original price (MRP) stored in USD equivalent
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Discount percent (0-100)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # Selling price computed from original_price and discount_percent (stored in USD)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

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
            models.Index(fields=['team', 'status']),
            models.Index(fields=['category']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        if self.team:
            return f"{self.name} by {self.team.name}"
        return f"{self.name} by {self.artisan.user.get_full_name()}"

    def save(self, *args, **kwargs):
        """Maintain INR range and compute selling price from original price + discount.

        Behavior:
        - Clamp original_price (in USD storage) to the INR range defined in settings.
        - If discount_percent is set, compute selling_price = original_price * (1 - discount/100).
        - Ensure original_price > selling_price; if equality occurs, ensure selling_price is slightly lower.
        - Keep the legacy `price` field in sync with selling_price for backward compatibility.
        """
        from decimal import Decimal, ROUND_HALF_UP
        from django.conf import settings

        try:
            rate = Decimal(getattr(settings, 'USD_TO_INR_RATE', 83))
            min_inr = Decimal(getattr(settings, 'MIN_PRICE_INR', 500))
            max_inr = Decimal(getattr(settings, 'MAX_PRICE_INR', 5000))

            # Compute USD bounds
            min_usd = (min_inr / rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            max_usd = (max_inr / rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # If original_price provided, clamp it into USD bounds
            if self.original_price is not None:
                op = Decimal(self.original_price)
                if op < min_usd:
                    op = min_usd
                elif op > max_usd:
                    op = max_usd
                self.original_price = op.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            else:
                # If original_price absent but legacy price exists, use that as original
                if self.price is not None:
                    self.original_price = Decimal(self.price)

            # Normalize discount percent
            if self.discount_percent is not None:
                dp = Decimal(self.discount_percent)
                if dp < Decimal('0'):
                    dp = Decimal('0')
                if dp > Decimal('100'):
                    dp = Decimal('100')
                self.discount_percent = dp.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # Compute selling_price
            if self.original_price is not None and self.discount_percent is not None:
                op = Decimal(self.original_price)
                dp = Decimal(self.discount_percent)
                sp = (op * (Decimal('100') - dp) / Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                # Ensure selling < original
                if sp >= op:
                    sp = (op - Decimal('0.01')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                self.selling_price = sp
            else:
                # Fallback: if selling_price absent, try to set from legacy price
                if self.selling_price is None and self.price is not None:
                    self.selling_price = Decimal(self.price)

            # Ensure selling_price in USD clamped into bounds as well
            if self.selling_price is not None:
                spv = Decimal(self.selling_price)
                if spv < min_usd:
                    spv = min_usd
                elif spv > max_usd:
                    spv = max_usd
                self.selling_price = spv.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            # Keep legacy `price` field in sync
            if self.selling_price is not None:
                self.price = self.selling_price

            # Ensure cost_price not greater than original if cost_price is provided
            if self.cost_price:
                cp = Decimal(self.cost_price)
                if self.original_price is not None and cp > Decimal(self.original_price):
                    self.cost_price = Decimal(self.original_price)
                # clamp cost_price into bounds
                if cp < min_usd:
                    self.cost_price = min_usd
                elif cp > max_usd:
                    self.cost_price = max_usd
        except Exception:
            pass

        super().save(*args, **kwargs)
    
    def in_stock(self):
        return self.quantity_in_stock > 0
    
    def discount_percentage(self):
        """Calculate discount if cost_price exists"""
        if self.cost_price and self.cost_price < self.price:
            return int(((self.price - self.cost_price) / self.price) * 100)
        return 0
    
    def get_owner_name(self):
        """Get the name of the product owner (team or artisan)"""
        if self.team:
            return self.team.name
        return self.artisan.user.get_full_name()


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
