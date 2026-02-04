from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model




User = get_user_model() # Returns the active user model defined in AUTH_USER_MODEL (settings.py)

# Why UserCreationForm?
# => UserCreationForm ensures secure password handling and validation out of the box.Already includes:password1, password2 ,Password matching validation,Password strength validation


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter First Name",
        }) # A widget controls how a form field is rendered in HTML.
          # Field → handles data + validation
          # first_name → field name, forms.charfield → field 
          # Widget → handles HTML input element
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Last Name",
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email address'
        })
    )
    
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Phone Number",
        })
    )
    
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )
    # Why not write HTML directly in templates?
    # => Form controls structure, template controls layout, Same form used in multiple templates , Less logic and repetition , Change style once, affects everywhere

    class Meta:
        model = User  # replace with your user model
        fields = ("first_name", "last_name", "email", "phone_number", "password1", "password2")


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    
