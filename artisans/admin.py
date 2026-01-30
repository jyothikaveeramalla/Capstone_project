from django.contrib import admin
from .models import ArtisanProfile, ArtisanTeam, ArtisanTeamMember


@admin.register(ArtisanProfile)
class ArtisanProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'craft_type', 'team', 'rating', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at', 'rating', 'team')
    search_fields = ('user__email', 'user__first_name', 'craft_type')
    readonly_fields = ('rating', 'total_products', 'total_sales', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User Info', {
            'fields': ('user',)
        }),
        ('Team', {
            'fields': ('team',)
        }),
        ('Craft Details', {
            'fields': ('craft_type', 'description', 'years_of_experience', 'workshop_location', 'website')
        }),
        ('Social Links', {
            'fields': ('instagram_handle', 'facebook_link')
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


@admin.register(ArtisanTeam)
class ArtisanTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'get_member_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Team Info', {
            'fields': ('name', 'owner', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = 'Members'


@admin.register(ArtisanTeamMember)
class ArtisanTeamMemberAdmin(admin.ModelAdmin):
    list_display = ('get_user_name', 'team', 'role', 'joined_at')
    list_filter = ('role', 'team', 'joined_at')
    search_fields = ('user__email', 'user__first_name', 'team__name')
    readonly_fields = ('joined_at',)
    
    fieldsets = (
        ('Member Info', {
            'fields': ('team', 'user', 'role')
        }),
        ('Timestamps', {
            'fields': ('joined_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_name(self, obj):
        return obj.user.get_full_name()
    get_user_name.short_description = 'User'
