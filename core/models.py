from django.db import models

class PageContent(models.Model):
    """
    Editable page content for home, about, etc.
    """
    PAGE_CHOICES = (
        ('home', 'Home'),
        ('about', 'About'),
        ('how_it_works', 'How It Works'),
        ('impact', 'Impact'),
        ('contact', 'Contact'),
    )
    
    page_name = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    hero_image = models.ImageField(upload_to='pages/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_pagecontent'
        verbose_name = 'Page Content'
        verbose_name_plural = 'Page Contents'
    
    def __str__(self):
        return f"{self.page_name.replace('_', ' ').title()} Page"


class Testimonial(models.Model):
    """
    Customer testimonials
    """
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('artisan', 'Artisan'),
        ('influencer', 'Influencer'),
    )
    
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
    text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_testimonial'
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Testimonial by {self.name}"


class Contact(models.Model):
    """
    Contact form submissions
    """
    STATUS_CHOICES = (
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('closed', 'Closed'),
    )
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    reply = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_contact'
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Contact from {self.name}"


class StatisticBlock(models.Model):
    """
    Statistics shown on home page
    """
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=100)  # e.g., "500+", "50K"
    icon = models.CharField(max_length=50, blank=True, null=True)  # For emoji or icon class
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'core_statistic'
        verbose_name = 'Statistic'
        verbose_name_plural = 'Statistics'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.label}: {self.value}"
