"""
Views for URL app with full authentication and features
"""
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse, HttpResponseForbidden, Http404
from django.db.models import Count, Q
from .models import ShortenedURL, URLClick
from .forms import URLForm, URLEditForm


def home(request):
    """
    Home page - landing page for non-authenticated users
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'app/home.html')



@login_required
def create_url(request):
    """
    Create a new shortened URL
    """
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            try:
                # Get form data
                original_url = form.cleaned_data['url']
                custom_key = form.cleaned_data.get('custom_key', '').strip()
                expires_in_days = form.cleaned_data.get('expires_in_days')
                generate_qr = form.cleaned_data.get('generate_qr', False)
                
                # Calculate expiration date
                expires_at = None
                if expires_in_days:
                    expires_at = timezone.now() + timedelta(days=expires_in_days)
                
                # Create shortened URL
                shortened = ShortenedURL.create_short_url(
                    user=request.user,
                    original_url=original_url,
                    custom_key=custom_key if custom_key else None,
                    expires_at=expires_at
                )
                
                # Generate QR code if requested
                if generate_qr:
                    shortened.generate_qr_code(request)
                
                messages.success(request, 'Short URL created successfully!')
                return redirect('url_detail', pk=shortened.pk)
                
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = URLForm()
    
    return render(request, 'app/create_url.html', {'form': form})


@login_required
def url_detail(request, pk):
    """
    View details and analytics for a specific URL
    """
    url = get_object_or_404(ShortenedURL, pk=pk, user=request.user)
    
    # Get recent clicks
    recent_clicks = url.clicks.all()[:20]
    
    # Build the full short URL
    short_url = request.build_absolute_uri(reverse('redirect_url', kwargs={'short_key': url.short_key}))
    
    # Check if expired
    is_expired = url.is_expired()
    
    context = {
        'url': url,
        'short_url': short_url,
        'recent_clicks': recent_clicks,
        'is_expired': is_expired,
    }
    
    return render(request, 'app/url_detail.html', context)


@login_required
def edit_url(request, pk):
    """
    Edit an existing shortened URL
    """
    url = get_object_or_404(ShortenedURL, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = URLEditForm(request.POST, instance=url)
        if form.is_valid():
            # Update URL
            url = form.save(commit=False)
            
            # Update expiration if provided
            expires_in_days = form.cleaned_data.get('expires_in_days')
            if expires_in_days:
                url.expires_at = timezone.now() + timedelta(days=expires_in_days)
            
            url.save()
            messages.success(request, 'URL updated successfully!')
            return redirect('url_detail', pk=url.pk)
    else:
        form = URLEditForm(instance=url)
    
    context = {
        'form': form,
        'url': url,
    }
    
    return render(request, 'app/edit_url.html', context)


@login_required
def delete_url(request, pk):
    """
    Delete a shortened URL
    """
    url = get_object_or_404(ShortenedURL, pk=pk, user=request.user)
    
    if request.method == 'POST':
        url.delete()
        messages.success(request, 'URL deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'app/delete_url.html', {'url': url})


@login_required
def generate_qr_view(request, pk):
    """
    Generate QR code for an existing URL
    """
    url = get_object_or_404(ShortenedURL, pk=pk, user=request.user)
    
    if not url.qr_code:
        url.generate_qr_code(request)
        messages.success(request, 'QR code generated successfully!')
    else:
        messages.info(request, 'QR code already exists.')
    
    return redirect('url_detail', pk=url.pk)


def redirect_url(request, short_key):
    """
    Redirect from short URL to original URL
    Track analytics
    """
    url = get_object_or_404(ShortenedURL, short_key=short_key)
    
    # Check if expired
    if url.is_expired():
        return render(request, 'app/expired.html', {'url': url}, status=410)
    
    # Increment click counter
    url.increment_click_count()
    
    # Track detailed click analytics
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    referrer = request.META.get('HTTP_REFERER', '')
    
    URLClick.objects.create(
        url=url,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer
    )
    
    # Redirect to original URL
    return redirect(url.original_url)


@login_required
def check_custom_key(request):
    """
    AJAX endpoint to check if a custom key is available
    """
    key = request.GET.get('key', '').strip()
    
    if not key:
        return JsonResponse({'available': False, 'message': 'Key cannot be empty'})
    
    if len(key) < 3:
        return JsonResponse({'available': False, 'message': 'Key must be at least 3 characters'})
    
    available = ShortenedURL.is_key_available(key)
    
    return JsonResponse({
        'available': available,
        'message': 'Available!' if available else 'Already taken'
    })


def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip