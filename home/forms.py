"""
Forms for URL Shortener
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import URLValidator
from .models import ShortenedURL
import re




class URLForm(forms.Form):
    """
    Form for creating and editing shortened URLs
    """
    url = forms.URLField(
        max_length=2048,
        label='Long URL',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com/very-long-url',
            'autocomplete': 'off',
        }),
        validators=[URLValidator()],
        error_messages={
            'required': 'Please enter a URL',
            'invalid': 'Please enter a valid URL (including http:// or https://)',
        }
    )
    
    custom_key = forms.CharField(
        max_length=50,
        required=False,
        label='Custom Short URL (optional)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'my-custom-url',
            'autocomplete': 'off',
        }),
        help_text='Leave empty for auto-generated key. Use only letters and numbers.'
    )
    
    expires_in_days = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=365,
        label='Expires in (days)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Leave empty for no expiration',
        }),
        help_text='Number of days until this link expires (optional)'
    )
    
    generate_qr = forms.BooleanField(
        required=False,
        initial=False,
        label='Generate QR Code',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        })
    )
    
    def clean_custom_key(self):
        """
        Validate custom key
        """
        custom_key = self.cleaned_data.get('custom_key', '').strip()
        
        if not custom_key:
            return custom_key
        
        # Check if alphanumeric and hyphens/underscores only
        if not re.match(r'^[a-zA-Z0-9_-]+$', custom_key):
            raise forms.ValidationError(
                'Custom URL can only contain letters, numbers, hyphens, and underscores'
            )
        
        # Check minimum length
        if len(custom_key) < 3:
            raise forms.ValidationError(
                'Custom URL must be at least 3 characters long'
            )
        
        # Check if available
        if not ShortenedURL.is_key_available(custom_key):
            raise forms.ValidationError(
                'This custom URL is already taken. Please choose another.'
            )
        
        return custom_key


class URLEditForm(forms.ModelForm):
    """
    Form for editing existing URLs
    """
    expires_in_days = forms.IntegerField(
        required=False,
        min_value=1,
        max_value=365,
        label='Expires in (days)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Leave empty for no expiration',
        }),
        help_text='Number of days from now until this link expires (optional)'
    )
    
    class Meta:
        model = ShortenedURL
        fields = ['original_url']
        widgets = {
            'original_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/very-long-url',
            }),
        }
        labels = {
            'original_url': 'Long URL',
        }