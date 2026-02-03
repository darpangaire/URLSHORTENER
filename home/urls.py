"""
URL patterns for URL Shortener app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    

    
    # Dashboard and URL management (authenticated)

    path('create/', views.create_url, name='create_url'),
    path('url/<int:pk>/', views.url_detail, name='url_detail'),
    path('url/<int:pk>/edit/', views.edit_url, name='edit_url'),
    path('url/<int:pk>/delete/', views.delete_url, name='delete_url'),
    path('url/<int:pk>/qr/', views.generate_qr_view, name='generate_qr'),
    
    # AJAX endpoints
    path('api/check-key/', views.check_custom_key, name='check_custom_key'),
    
    # Redirect (must be last to catch all short keys)
    path('<str:short_key>/', views.redirect_url, name='redirect_url'),
]