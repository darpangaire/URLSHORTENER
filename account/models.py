from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

# why BaseUserManager?
# It handles user creation logic for custom user models.Required when using AbstractBaseUser.

# Why needed?
# Django doesn’t know: How to create users, which fields are mandatory. so manager defines this logic explicitly.

class MyAccountManager(BaseUserManager):
  def create_user(self,first_name,last_name,username,email,password=None):
    if not email:
      raise ValueError("User must have an email address")
    if not username:
      raise ValueError("User must have a username")
    
    user = self.model(
      email = self.normalize_email(email),# TEST@GMAIL.COM → TEST@gmail.com
      username = username,
      first_name = first_name,
      last_name = last_name,

    )
    user.is_active = True
    
    user.set_password(password) # Password is hashed
    user.save(using=self._db) # self._db supports multiple databases
    return user
  
  def create_superuser(self,first_name,last_name,username,email,password):
    user = self.create_user(
      email = email,
      password=password,
      username = username,
      first_name = first_name,
      last_name = last_name,
      
    ) # Why reuse? => Avoids code duplication


    user.is_admin = True
    user.is_staff = True
    user.is_active = True
    user.is_superadmin = True
    user.save(using=self._db)
    return user
  
# why AbstractBaseUser?
# It provides core authentication features includes password field,last_login,set_password() (hashes passwords),check_password(). It gives full control over fields. Allows email-based authentication instead of username-based. Best practice for production apps.
class Account(AbstractBaseUser):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=50, unique=True)
  email = models.EmailField(max_length=100,unique=True)
  phone_number = models.CharField(max_length=50)
  
  # required fields
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now_add=True)
  is_admin = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  is_superadmin = models.BooleanField(default=False)

  objects = MyAccountManager() 

  USERNAME_FIELD = 'email'
  
  REQUIRED_FIELDS = ['first_name','last_name','username']
  
  def __str__(self):
    return self.email
  
  def has_perm(self,perm,obj=None):
    return self.is_admin
  
  def has_module_perms(self,add_label):
    return True
 

 
