from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from .forms import RegistrationForm, LoginForm
from home.models import ShortenedURL

def register_view(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    
    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
    else:
        form = LoginForm()
    
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    """
    User dashboard - view and manage URLs
    """
    # Get user's URLs
    urls = ShortenedURL.objects.filter(user=request.user).select_related('user')
    
    # Statistics
    total_urls = urls.count()
    total_clicks = sum(url.click_count for url in urls)
    active_urls = urls.filter(Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())).count()
    expired_urls = total_urls - active_urls
    
    # Sort and filter
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by in ['created_at', '-created_at', 'click_count', '-click_count', 'original_url']:
        urls = urls.order_by(sort_by)
    
    context = {
        'urls': urls,
        'total_urls': total_urls,
        'total_clicks': total_clicks,
        'active_urls': active_urls,
        'expired_urls': expired_urls,
        'current_sort': sort_by,
    }
    
    return render(request, 'account/dashboard.html', context)
