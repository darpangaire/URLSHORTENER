from django.urls import path,include
from .views import register,Login
urlpatterns = [
  path('register/',register,name='register'),
  path('login/',Login,name='login'),
  
]


