from django.contrib import admin
from .models import ArtisanProfile


@admin.register(ArtisanProfile)
class ArtisanProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'craft_type', 'rating', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at', 'rating')
    search_fields = ('user__email', 'user__first_name', 'craft_type')
    readonly_fields = ('rating', 'total_products', 'total_sales', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Craft Details', {
            'fields': ('craft_type', 'description', 'years_of_experience', 'workshop_location', 'website')
        }),
        ('Social Links', {
            'fields': ('social_links',)
        }),
        ('Stats', {
            'fields': ('rating', 'total_products', 'total_sales'),
            'classes': ('collapse',)
        }),
        ('Featured', {
            'fields': ('is_featured',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Artisan Name'
