from django.contrib import admin
from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)
    
    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'artisan', 'category', 'price', 'quantity_in_stock', 'status', 'is_eco_friendly', 'rating', 'created_at')
    list_filter = ('status', 'is_eco_friendly', 'created_at', 'category')
    search_fields = ('name', 'artisan__user__email', 'description')
    readonly_fields = ('rating', 'review_count', 'sold_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('artisan', 'name', 'description', 'category', 'image')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'cost_price', 'quantity_in_stock')
        }),
        ('Details', {
            'fields': ('material', 'dimensions', 'weight', 'is_eco_friendly')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Stats', {
            'fields': ('rating', 'review_count', 'sold_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'customer', 'rating', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = ('title', 'product__name', 'customer__email')
    readonly_fields = ('helpful_count', 'created_at', 'updated_at')
