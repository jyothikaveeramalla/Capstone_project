from django.contrib import admin
from .models import InfluencerProfile


@admin.register(InfluencerProfile)
class InfluencerProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'niche', 'total_followers', 'rating', 'is_verified', 'is_featured', 'created_at')
    list_filter = ('is_verified', 'is_featured', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'niche')
    readonly_fields = ('rating', 'total_collaborations', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Profile', {
            'fields': ('niche', 'bio', 'follower_count')
        }),
        ('Social Links', {
            'fields': ('social_links',)
        }),
        ('Collaboration', {
            'fields': ('collaboration_rate', 'total_collaborations')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_featured'),
        }),
        ('Stats', {
            'fields': ('rating',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Influencer Name'
