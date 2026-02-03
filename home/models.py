"""
Models for URL Shortener with full features
"""
from django.db import models
from django.conf import settings
from django.conf import settings
from django.utils import timezone
import string
import random
import qrcode
from io import BytesIO
from django.core.files import File

User = settings.AUTH_USER_MODEL


class ShortenedURL(models.Model):
    """
    Model to store shortened URLs with all required features:
    - User authentication
    - Custom short URLs
    - Expiration time
    - Analytics (click count)
    - QR code generation
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')
    original_url = models.URLField(max_length=2048, verbose_name='Original URL')
    short_key = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Short Key')
    custom_key = models.BooleanField(default=False, verbose_name='Is Custom Key')
    
    # Analytics
    click_count = models.IntegerField(default=0, verbose_name='Click Count')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Expiration
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name='Expires At')
    
    # QR Code
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True, verbose_name='QR Code')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Shortened URL'
        verbose_name_plural = 'Shortened URLs'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['short_key']),
        ]
    
    def __str__(self):
        return f"{self.short_key} -> {self.original_url[:50]}"
    
    @staticmethod
    def generate_short_key(length=None):
        """
        Generate a unique short key using base62 encoding
        Base62 uses: 0-9, a-z, A-Z (62 characters)
        """
        if length is None:
            length = getattr(settings, 'SHORT_URL_LENGTH', 6)
        
        # Base62 character set
        base62_chars = string.ascii_letters + string.digits
        
        max_attempts = 10
        for _ in range(max_attempts):
            # Generate random short key
            short_key = ''.join(random.choices(base62_chars, k=length))
            
            # Check if it's unique
            if not ShortenedURL.objects.filter(short_key=short_key).exists():
                return short_key
        
        # If we couldn't find a unique key in max_attempts, increase length
        return ShortenedURL.generate_short_key(length + 1)
    
    @staticmethod
    def is_key_available(key):
        """Check if a custom key is available"""
        return not ShortenedURL.objects.filter(short_key=key).exists()
    
    def increment_click_count(self):
        """Increment the click count for this URL"""
        self.click_count += 1
        self.save(update_fields=['click_count'])
    
    def is_expired(self):
        """Check if the URL has expired"""
        if self.expires_at is None:
            return False
        return timezone.now() > self.expires_at
    
    def generate_qr_code(self, request=None):
        """
        Generate QR code for the short URL
        """
        if request:
            # Build the full short URL
            short_url = request.build_absolute_uri(f'/{self.short_key}/')
        else:
            # Fallback to just the key
            short_url = self.short_key
        
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data
        qr.add_data(short_url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Save to model
        filename = f'qr_{self.short_key}.png'
        self.qr_code.save(filename, File(buffer), save=False)
        self.save(update_fields=['qr_code'])
        
        return self.qr_code
    
    @classmethod
    def create_short_url(cls, user, original_url, custom_key=None, expires_at=None):
        """
        Create a new shortened URL
        """
        # Use custom key if provided and available
        if custom_key:
            # Validate custom key
            if not cls.is_key_available(custom_key):
                raise ValueError("Custom key is already in use")
            
            # Validate format (alphanumeric only)
            if not all(c.isalnum() for c in custom_key):
                raise ValueError("Custom key must contain only letters and numbers")
            
            short_key = custom_key
            is_custom = True
        else:
            # Generate unique short key
            short_key = cls.generate_short_key()
            is_custom = False
        
        # Create and return new shortened URL
        return cls.objects.create(
            user=user,
            original_url=original_url,
            short_key=short_key,
            custom_key=is_custom,
            expires_at=expires_at
        )


class URLClick(models.Model):
    """
    Model to track individual clicks for detailed analytics
    """
    url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(max_length=2048, blank=True)
    
    class Meta:
        ordering = ['-clicked_at']
        verbose_name = 'URL Click'
        verbose_name_plural = 'URL Clicks'
    
    def __str__(self):
        return f"Click on {self.url.short_key} at {self.clicked_at}"