from django.contrib import admin # Django’s built-in admin site
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# Why UserAdmin?
# => Already handles: Password hashing, Permission fields, Groups, User-specific admin logic

# Why not admin.ModelAdmin?
# => Does not handle Password hashing, UserAdmin is built specifically for authentication models
class AccountAdmin(UserAdmin):
  list_display = ('email','username','first_name','last_name','last_login','date_joined','is_active') # Controls columns shown in admin list view
  
  # list_display_links = ('email','username','first_name','last_name')
  # Makes these fields clickable, Clicking opens the detail/edit page
  
  readonly_fields = ('last_login','date_joined')
  
  
  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'phone_number')}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superadmin')}),
    ('Important dates', {'fields': ('last_login', 'date_joined')}),
) # What is fieldsets? => Controls layout of fields in admin edit page
  list_filter = ('is_admin','is_staff','is_active') # Adds filters in right sidebar
  filter_horizontal = () # Used for ManyToMany fields to display a horizontal filter interface
  
  search_fields = ('email','username') # Adds a search box to the admin list view
  ordering = ('-date_joined',) # Default ordering of records in admin list view


admin.site.register(Account,AccountAdmin)


