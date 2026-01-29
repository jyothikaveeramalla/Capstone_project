from django.db import models
from accounts.models import User

class ArtisanProfile(models.Model):
    """
    Extended profile for artisan users
    """
    CRAFT_CATEGORIES = (
        ('textiles', 'Textiles & Weaving'),
        ('pottery', 'Pottery & Ceramics'),
        ('jewelry', 'Jewelry & Accessories'),
        ('woodwork', 'Woodwork & Carpentry'),
        ('metalwork', 'Metalwork'),
        ('painting', 'Painting & Art'),
        ('other', 'Other'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artisan_profile')
    craft_type = models.CharField(max_length=50, choices=CRAFT_CATEGORIES)
    description = models.TextField(help_text='Detailed description of your craft')
    years_of_experience = models.IntegerField(default=0)
    workshop_location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    instagram_handle = models.CharField(max_length=100, blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_products = models.IntegerField(default=0)
    total_sales = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'artisans_profile'
        verbose_name = 'Artisan Profile'
        verbose_name_plural = 'Artisan Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_craft_type_display()}"
