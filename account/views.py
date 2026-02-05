from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils import timezone
from .forms import RegistrationForm, LoginForm
from home.models import ShortenedURL
from django.contrib import messages
from django.contrib.auth import login
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from .forms import RegistrationForm, LoginForm


def register_view(request):
    """
    Handle user registration and log the user in after successful signup.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.is_active = True
                    user.save()
            except IntegrityError:
                form.add_error('email', 'An account with this email already exists.')
            else:
                login(request, user)
                messages.success(
                    request,
                    f"Welcome {user.first_name}! Your account has been created."
                )
                return redirect('dashboard')
    else:
        form = RegistrationForm()

    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    """
    Authenticate users using email and password.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(
                request,
                f"Welcome back, {user.first_name}!"
            )
            return redirect(request.POST.get('next') or 'dashboard')
        else:
            messages.error(request, 'Invalid email or password.')
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
