from django.contrib import admin
from .models import CollaborationRequest, ActiveCollaboration, CollaborationPost


@admin.register(CollaborationRequest)
class CollaborationRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'influencer_name', 'artisan_name', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'influencer__user__email', 'artisan__user__email')
    readonly_fields = ('created_at', 'updated_at')
    
    def influencer_name(self, obj):
        return obj.influencer.user.get_full_name()
    influencer_name.short_description = 'Influencer'
    
    def artisan_name(self, obj):
        return obj.artisan.user.get_full_name()
    artisan_name.short_description = 'Artisan'


class CollaborationPostInline(admin.TabularInline):
    model = CollaborationPost
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ActiveCollaboration)
class ActiveCollaborationAdmin(admin.ModelAdmin):
    list_display = ('title', 'influencer_name', 'artisan_name', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('title', 'influencer__user__email', 'artisan__user__email')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CollaborationPostInline]
    
    def influencer_name(self, obj):
        return obj.influencer.user.get_full_name()
    influencer_name.short_description = 'Influencer'
    
    def artisan_name(self, obj):
        return obj.artisan.user.get_full_name()
    artisan_name.short_description = 'Artisan'


@admin.register(CollaborationPost)
class CollaborationPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'collaboration', 'platform', 'created_at')
    list_filter = ('platform', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
