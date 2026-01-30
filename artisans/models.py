from django.db import models
from accounts.models import User
from django.utils.timezone import now

class ArtisanTeam(models.Model):
    """
    Team model to allow multiple artisans to work together and share products
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_teams')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'artisans_team'
        verbose_name = 'Artisan Team'
        verbose_name_plural = 'Artisan Teams'
    
    def __str__(self):
        return self.name
    
    def add_member(self, user, role='member'):
        """Add a user to the team"""
        member, created = ArtisanTeamMember.objects.get_or_create(
            team=self,
            user=user,
            defaults={'role': role}
        )
        return member, created
    
    def remove_member(self, user):
        """Remove a user from the team"""
        ArtisanTeamMember.objects.filter(team=self, user=user).delete()
    
    def get_members(self):
        """Get all team members"""
        return self.members.all()
    
    def has_member(self, user):
        """Check if user is a member of the team"""
        return self.members.filter(user=user).exists()


class ArtisanTeamMember(models.Model):
    """
    Team membership model for tracking artisans in teams
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    
    team = models.ForeignKey(ArtisanTeam, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'artisans_team_member'
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'
        unique_together = ('team', 'user')
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.team.name} ({self.role})"


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
    team = models.ForeignKey(ArtisanTeam, on_delete=models.SET_NULL, null=True, blank=True, related_name='artisans')
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
