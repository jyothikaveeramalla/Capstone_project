from django.contrib import admin
from .models import PageContent, Testimonial, Contact, StatisticBlock


@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'title', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'is_featured', 'is_published', 'created_at')
    list_filter = ('role', 'rating', 'is_featured', 'is_published', 'created_at')
    search_fields = ('name', 'text')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StatisticBlock)
class StatisticBlockAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'order')
    list_editable = ('order',)
    ordering = ('order',)
