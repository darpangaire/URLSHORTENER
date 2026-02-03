"""
Admin configuration for URL Shortener
"""
from django.contrib import admin
from .models import ShortenedURL, URLClick


@admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    """
    Admin interface for ShortenedURL model
    """
    list_display = ('short_key', 'user', 'original_url_truncated', 'click_count', 'custom_key', 'is_expired_display', 'created_at')
    list_filter = ('custom_key', 'created_at', 'user')
    search_fields = ('short_key', 'original_url', 'user__username')
    readonly_fields = ('short_key', 'created_at', 'updated_at', 'click_count', 'qr_code')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('URL Information', {
            'fields': ('user', 'original_url', 'short_key', 'custom_key')
        }),
        ('Analytics', {
            'fields': ('click_count',)
        }),
        ('Expiration', {
            'fields': ('expires_at',)
        }),
        ('QR Code', {
            'fields': ('qr_code',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def original_url_truncated(self, obj):
        """Display truncated original URL"""
        return obj.original_url[:50] + '...' if len(obj.original_url) > 50 else obj.original_url
    original_url_truncated.short_description = 'Original URL'
    
    def is_expired_display(self, obj):
        """Display expiration status"""
        if obj.expires_at is None:
            return '∞'
        return '✓ Expired' if obj.is_expired() else '✗ Active'
    is_expired_display.short_description = 'Status'


@admin.register(URLClick)
class URLClickAdmin(admin.ModelAdmin):
    """
    Admin interface for URLClick model
    """
    list_display = ('url', 'clicked_at', 'ip_address', 'referrer_truncated')
    list_filter = ('clicked_at',)
    search_fields = ('url__short_key', 'ip_address', 'referrer')
    readonly_fields = ('url', 'clicked_at', 'ip_address', 'user_agent', 'referrer')
    ordering = ('-clicked_at',)
    date_hierarchy = 'clicked_at'
    
    def referrer_truncated(self, obj):
        """Display truncated referrer"""
        if not obj.referrer:
            return '(direct)'
        return obj.referrer[:50] + '...' if len(obj.referrer) > 50 else obj.referrer
    referrer_truncated.short_description = 'Referrer'
    
    def has_add_permission(self, request):
        """Disable adding through admin"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Make read-only"""
        return False