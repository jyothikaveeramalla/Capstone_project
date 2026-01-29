from django.contrib import admin
from .models import Order, OrderItem, Shipment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product_name', 'product_price', 'subtotal')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'total_amount', 'order_status', 'payment_status', 'created_at')
    list_filter = ('order_status', 'payment_status', 'created_at')
    search_fields = ('order_id', 'customer__email')
    readonly_fields = ('order_id', 'subtotal', 'shipping_cost', 'tax', 'total_amount', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Info', {
            'fields': ('order_id', 'customer')
        }),
        ('Shipping Address', {
            'fields': ('shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country')
        }),
        ('Totals', {
            'fields': ('subtotal', 'shipping_cost', 'tax', 'total_amount')
        }),
        ('Status', {
            'fields': ('order_status', 'payment_status')
        }),
        ('Tracking', {
            'fields': ('tracking_number', 'estimated_delivery', 'delivered_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'tracking_number', 'carrier', 'status', 'shipped_date', 'delivered_date')
    list_filter = ('status', 'shipped_date', 'delivered_date')
    search_fields = ('tracking_number', 'order__order_id')
    readonly_fields = ('created_at', 'updated_at')
