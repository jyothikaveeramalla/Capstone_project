from django.db import models
from accounts.models import User
from artisans.models import ArtisanProfile
from influencers.models import InfluencerProfile

class CollaborationRequest(models.Model):
    """
    Collaboration requests sent by influencers to artisans
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    )
    
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE, related_name='sent_requests')
    artisan = models.ForeignKey(ArtisanProfile, on_delete=models.CASCADE, related_name='received_requests')
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    proposed_terms = models.TextField(help_text='Terms of collaboration')
    
    # Commission/Rate
    commission_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text='Influencer commission percentage on sales'
    )
    flat_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text='Flat rate for collaboration'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    message_from_influencer = models.TextField(blank=True, null=True)
    response_from_artisan = models.TextField(blank=True, null=True)
    
    attachment = models.FileField(upload_to='collaboration_files/', blank=True, null=True)
    
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaborations_request'
        verbose_name = 'Collaboration Request'
        verbose_name_plural = 'Collaboration Requests'
        unique_together = ['influencer', 'artisan']  # Prevent duplicate requests
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"Collaboration: {self.influencer.user.get_full_name()} → {self.artisan.user.get_full_name()}"


class ActiveCollaboration(models.Model):
    """
    Active/ongoing collaborations between influencers and artisans
    """
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated'),
    )
    
    influencer = models.ForeignKey(InfluencerProfile, on_delete=models.CASCADE, related_name='active_collaborations')
    artisan = models.ForeignKey(ArtisanProfile, on_delete=models.CASCADE, related_name='active_collaborations')
    
    collaboration_request = models.OneToOneField(
        CollaborationRequest, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='collaboration'
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Financial Terms
    commission_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    flat_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Duration
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Metrics
    total_products_promoted = models.IntegerField(default=0)
    total_sales_generated = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    posts_published = models.IntegerField(default=0)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    is_exclusive = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaborations_active'
        verbose_name = 'Active Collaboration'
        verbose_name_plural = 'Active Collaborations'
        unique_together = ['influencer', 'artisan']  # One active collaboration per pair
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Collab: {self.influencer.user.get_full_name()} ↔ {self.artisan.user.get_full_name()}"


class CollaborationPost(models.Model):
    """
    Posts/content created by influencers for artisan collaborations
    """
    collaboration = models.ForeignKey(
        ActiveCollaboration, on_delete=models.CASCADE, related_name='posts'
    )
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='collaboration_posts/', null=True, blank=True)
    
    platform = models.CharField(
        max_length=50,
        choices=[
            ('instagram', 'Instagram'),
            ('youtube', 'YouTube'),
            ('facebook', 'Facebook'),
            ('blog', 'Blog'),
        ],
        default='instagram'
    )
    
    url = models.URLField(null=True, blank=True, help_text='Link to the post')
    
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'collaborations_post'
        verbose_name = 'Collaboration Post'
        verbose_name_plural = 'Collaboration Posts'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return f"Post: {self.title} on {self.platform}"
