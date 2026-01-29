from django.db import models
from accounts.models import User

class InfluencerProfile(models.Model):
    """
    Extended profile for influencer users
    """
    NICHE_CHOICES = (
        ('fashion', 'Sustainable Fashion'),
        ('lifestyle', 'Eco-Lifestyle'),
        ('art', 'Art & Culture'),
        ('handmade', 'Handmade & DIY'),
        ('wellness', 'Wellness & Beauty'),
        ('other', 'Other'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='influencer_profile')
    niche = models.CharField(max_length=50, choices=NICHE_CHOICES)
    bio = models.TextField(max_length=1000, help_text='Your professional bio')
    follower_count = models.IntegerField(default=0)
    
    # Social Links
    instagram_handle = models.CharField(max_length=100, blank=True, null=True)
    instagram_followers = models.IntegerField(default=0)
    youtube_handle = models.CharField(max_length=100, blank=True, null=True)
    youtube_subscribers = models.IntegerField(default=0)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_handle = models.CharField(max_length=100, blank=True, null=True)
    personal_website = models.URLField(blank=True, null=True)
    
    # Rating & Stats
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_collaborations = models.IntegerField(default=0)
    collaboration_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text='Collaboration fee as percentage')
    
    is_verified = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'influencers_profile'
        verbose_name = 'Influencer Profile'
        verbose_name_plural = 'Influencer Profiles'
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_niche_display()}"
    
    def total_followers(self):
        """Calculate total followers across all platforms"""
        return self.instagram_followers + self.youtube_subscribers
