# URL Shortener - Django Web Application

A full-featured URL shortener web application built with Django, featuring user authentication, custom short URLs, analytics, QR code generation, and link expiration.

## 🎯 Project Overview

This is a complete URL shortener application developed as part of an interview assignment. It demonstrates proficiency in Django development, user authentication, database design, and creating a polished user interface.

## ✨ Features Implemented

### Core Requirements ✅

1. **User Authentication**
   - User registration with email validation
   - Secure login/logout functionality
   - Password validation and hashing
   - Session management
   - Protected routes (only authenticated users can create/manage URLs)

2. **URL Shortening**
   - Base62 encoding algorithm for short key generation
   - Automatic generation of 6-character unique keys
   - Uses characters: `0-9`, `a-z`, `A-Z` (62 total)
   - Collision detection and retry mechanism
   - Automatic redirect from short URL to original URL

3. **URL Management**
   - View all created short URLs in dashboard
   - Edit existing URLs (change destination)
   - Delete URLs with confirmation
   - Sortable URL list (by date, clicks)
   - Visual indicators for custom vs auto-generated keys

4. **Analytics**
   - Click counter for each URL
   - Detailed click tracking (timestamp, IP, referrer, user agent)
   - Recent clicks history
   - Dashboard statistics:
     - Total URLs created
     - Total clicks across all URLs
     - Active vs expired URLs count

5. **User Interface**
   - Clean, modern design using Bootstrap 5
   - Responsive layout (works on mobile, tablet, desktop)
   - Gradient color scheme with smooth animations
   - Icon integration (Bootstrap Icons)
   - Alert messages for user feedback
   - Intuitive navigation

### Bonus Features ✅

1. **Custom Short URLs**
   - Users can specify custom short keys
   - Live availability checking (AJAX)
   - Validation (alphanumeric, min 3 chars)
   - Visual indicators for custom URLs
   - Duplicate prevention

2. **Expiration Time**
   - Optional expiration date setting (days from now)
   - Visual countdown to expiration
   - Expired URL page with friendly message
   - Automatic blocking of expired links
   - Expired vs active status in dashboard

3. **QR Code Generation**
   - Generate QR codes for any short URL
   - Download QR code as PNG image
   - QR codes stored in media folder
   - Optional generation during URL creation
   - Generate QR code after creation



### Database Models

#### ShortenedURL Model
- `user` - ForeignKey to User (owner)
- `original_url` - The long URL to redirect to
- `short_key` - Unique short identifier
- `custom_key` - Boolean (custom vs auto-generated)
- `click_count` - Total clicks
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp
- `expires_at` - Optional expiration date
- `qr_code` - ImageField for QR code

#### URLClick Model (Analytics)
- `url` - ForeignKey to ShortenedURL
- `clicked_at` - Click timestamp
- `ip_address` - Client IP
- `user_agent` - Browser/device info
- `referrer` - Source URL

### Key Algorithms

#### Base62 Short Key Generation
```python
def generate_short_key(length=6):
    # Character set: 0-9, a-z, A-Z
    base62_chars = string.ascii_letters + string.digits
    
    # Generate random key
    for _ in range(10):  # Max attempts
        key = ''.join(random.choices(base62_chars, k=length))
        if not exists(key):
            return key
    
    # Increase length if no unique key found
    return generate_short_key(length + 1)
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning repository)

### Step 1: Clone Repository

```bash
git clone https://github.com/darpangaire/URLSHORTENER.git
cd URLSHORTENER
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```
Follow prompts to create admin account for accessing Django admin panel.

### Step 6: Run Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## 📖 Usage Guide

### For End Users

1. **Register an Account**
   - Visit http://127.0.0.1:8000/
   - Click "Register"
   - Fill in firstname, lastname, phonenumber, email, and password
   - Submit to create account

2. **Login**
   - Click "Login" in navigation
   - Enter credentials
   - Redirected to dashboard

3. **Create a Short URL**
   - Click "Create URL" in navigation
   - Enter long URL
   - (Optional) Enter custom short key
   - (Optional) Set expiration days
   - (Optional) Check "Generate QR Code"
   - Click "Create Short URL"

4. **Manage URLs**
   - View all URLs in dashboard
   - Sort by date or clicks
   - View details, edit, or delete any URL
   - See analytics and recent clicks

5. **Share Short URLs**
   - Copy short URL from dashboard or detail page
   - Share via social media, email, etc.
   - Download QR code for offline sharing

### For Developers

#### Admin Interface

Access Django admin at: http://127.0.0.1:8000/admin/

Features:
- View all shortened URLs
- See all click records
- Search and filter URLs
- Manage users

#### API Endpoints

- `GET /` - Home page
- `POST /register/` - User registration
- `POST /login/` - User login
- `GET /logout/` - User logout
- `GET /dashboard/` - User dashboard (auth required)
- `POST /create/` - Create short URL (auth required)
- `GET /url/<id>/` - URL details (auth required)
- `POST /url/<id>/edit/` - Edit URL (auth required)
- `POST /url/<id>/delete/` - Delete URL (auth required)
- `GET /url/<id>/qr/` - Generate QR code (auth required)
- `GET /api/check-key/` - Check custom key availability (AJAX)
- `GET /<short_key>/` - Redirect to original URL

## 🧪 Testing

### Manual Testing Checklist

- [ ] User can register new account
- [ ] User can login with credentials
- [ ] User can logout
- [ ] Authenticated user can create short URL
- [ ] Short URL redirects to original URL
- [ ] Click counter increments on each visit
- [ ] Custom short URLs work correctly
- [ ] Custom key availability check works (AJAX)
- [ ] URL expiration works
- [ ] Expired URLs show appropriate message
- [ ] QR code generation works
- [ ] User can edit URL destination
- [ ] User can delete URL
- [ ] Dashboard shows correct statistics
- [ ] Sorting URLs works (by date, clicks)
- [ ] Responsive design works on mobile
- [ ] Form validation works properly

### Testing with Django Shell

```bash
python manage.py shell
```

```python
from shortener.models import ShortenedURL
from django.contrib.auth.models import User

# Create test user
user = User.objects.create_user('testuser', 'test@example.com', 'password123')

# Create short URL
url = ShortenedURL.create_short_url(
    user=user,
    original_url='https://www.example.com/long-url',
    custom_key='custom'  # Optional
)

# Test key generation
key = ShortenedURL.generate_short_key()
print(f"Generated key: {key}")

# Check availability
available = ShortenedURL.is_key_available('test')
print(f"Key 'test' available: {available}")
```

## 🔒 Security Considerations

### Implemented Security Features

1. **Authentication & Authorization**
   - Django's built-in authentication system
   - Password hashing (PBKDF2)
   - CSRF protection on all forms
   - Login required decorators
   - User ownership validation

2. **Input Validation**
   - URL validation (URLValidator)
   - Custom key format validation
   - XSS protection (Django templates auto-escape)
   - SQL injection protection (Django ORM)

3. **Session Security**
   - Secure session cookies
   - Session expiration
   - Logout functionality

### Production Recommendations

Before deploying to production:

1. **Change Secret Key**
   ```python
   # In settings.py
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

2. **Disable Debug Mode**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

3. **Use Production Database**
   - Switch from SQLite to PostgreSQL/MySQL
   - Configure database credentials via environment variables

4. **Enable HTTPS**
   - Configure SSL certificate
   - Set SECURE_SSL_REDIRECT = True

5. **Set Up Static Files**
   ```bash
   python manage.py collectstatic
   ```

6. **Add Rate Limiting**
   - Implement rate limiting for URL creation
   - Prevent abuse and spam

7. **Set Up Logging**
   - Configure Django logging
   - Monitor errors and suspicious activity

## 🎨 Design Choices

### UI/UX Decisions

1. **Color Scheme**: Purple gradient theme for modern, professional look
2. **Icons**: Bootstrap Icons for consistent, recognizable actions
3. **Responsiveness**: Mobile-first design using Bootstrap grid
4. **Feedback**: Toast messages and inline validation for user guidance
5. **Animations**: Subtle hover effects and transitions for polish

### Technical Decisions

1. **Base62 Encoding**: More URL-friendly than base64, excludes special characters
2. **6-Character Keys**: Balance between short URLs and collision probability (56B combinations)
3. **SQLite**: Simple setup for development, easily switched to production DB
4. **Bootstrap 5**: Rapid development, proven responsive framework
5. **QR Code Storage**: Saved as images for reliability and offline access



## 🐛 Known Limitations

1. **Rate Limiting**: Not implemented - could be abused in production
2. **Email Verification**: Registration doesn't require email confirmation
3. **Password Reset**: No password recovery mechanism
4. **Bulk Operations**: No bulk delete or export functionality
5. **Advanced Analytics**: Limited to click count and basic tracking


## 📝 Code Quality


### Code Organization

- Models contain business logic (key generation, validation)
- Views handle HTTP requests/responses
- Forms manage data validation
- Templates handle presentation
- Admin provides management interface

## 🤝 Contributing

This is an interview project, but suggestions are welcome!

## 📄 License

This project is created for educational/interview purposes.

## 👤 Author

Developed as part of a technical interview assignment.

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Documentation
- Python QRCode Library
- Bootstrap Icons

---

**Note**: This README provides complete documentation for setup, usage, and understanding of the project. All required and bonus features have been implemented with attention to code quality, user experience, and best practices.
