from django.urls import path,include
from .views import register_view, login_view, logout_view, dashboard
urlpatterns = [
  path('register/', register_view, name='register'),
  path('login/', login_view, name='login'),
  path('logout/', logout_view, name='logout'),
  path('dashboard/', dashboard, name='dashboard'),
  
]


