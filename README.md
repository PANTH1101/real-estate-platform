# 🏠 Real Estate Platform

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2.29-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![DRF](https://img.shields.io/badge/DRF-3.17-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A comprehensive real estate platform with modern API architecture and legacy UI support**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## 🎯 Overview

**RealEstateHub** is a full-featured real estate platform built with Django that combines a modern RESTful API architecture with a traditional server-rendered UI. The platform facilitates property listings, buyer-seller interactions, payment processing, and comprehensive property management.

### Key Highlights

- 🏢 **Multiple Property Types**: Apartments, Villas, Plots, Commercial Offices, and Shops
- 🗺️ **Interactive Maps**: Leaflet.js integration with location search and picker
- 💳 **Payment Integration**: Razorpay payment gateway for secure transactions
- 🔐 **Dual Authentication**: JWT-based API auth + Google OAuth for legacy UI
- 📧 **Email Verification**: OTP-based lead verification system
- 📊 **Admin Dashboard**: Comprehensive statistics and property management
- 🎨 **Responsive Design**: Mobile-friendly interface
- 🔌 **RESTful API**: Complete API for modern frontend integration

---

## ✨ Features

### For Buyers 👥

- **Property Browsing**
  - Advanced search and filtering
  - Multiple property type support
  - Interactive map view with location markers
  - High-quality image galleries
  - Detailed property specifications

- **User Account**
  - Secure registration and login
  - Email verification
  - Profile management
  - Wishlist functionality
  - Enquiry tracking

- **Property Enquiries**
  - OTP-based email verification
  - Direct seller contact after verification
  - Enquiry history and status tracking

### For Sellers 🏗️

- **Property Management**
  - Easy property listing creation
  - Multiple image upload support
  - Interactive map-based location picker
  - Location search by address/landmark
  - Type-specific property fields
  - Draft and preview functionality

- **Dashboard**
  - Property performance analytics
  - Enquiry management
  - Payment tracking
  - Quick edit and update

- **Authentication**
  - Google OAuth integration
  - Secure seller verification

### For Administrators 👨‍💼

- **Admin Panel**
  - Property approval workflow
  - Pending/live property statistics
  - Payment monitoring
  - User management
  - Amenity management

- **Content Management**
  - Add/edit/delete amenities
  - Property moderation
  - User role management

### Technical Features 🔧

- **RESTful API**
  - JWT authentication
  - Token refresh mechanism
  - Comprehensive endpoints
  - Filtering and pagination
  - CORS support

- **Map Integration**
  - Leaflet.js with OpenStreetMap
  - Interactive location picker
  - Address search (Nominatim)
  - Draggable markers
  - Coordinate storage

- **Payment Processing**
  - Razorpay integration
  - Secure payment flow
  - Transaction tracking
  - Success/failure handling

- **Email System**
  - OTP generation and verification
  - Email notifications
  - Configurable SMTP settings

---

## 🛠️ Tech Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Core programming language |
| **Django** | 4.2.29 | Web framework |
| **Django REST Framework** | 3.17.1 | API development |
| **SimpleJWT** | 5.5.1 | JWT authentication |
| **django-filter** | 25.1 | API filtering |
| **django-cors-headers** | 4.9.0 | CORS handling |
| **Pillow** | 12.1.1 | Image processing |
| **Razorpay** | 2.0.1 | Payment gateway |
| **python-dotenv** | 1.2.2 | Environment management |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5/CSS3** | UI structure and styling |
| **JavaScript** | Client-side interactivity |
| **Leaflet.js** | Interactive maps |
| **OpenStreetMap** | Map tiles and data |
| **Nominatim** | Geocoding service |

### Database

- **SQLite** (Development) - Default, zero-configuration
- **MySQL** (Production) - Scalable, production-ready

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
├──────────────────────┬──────────────────────────────────────┤
│   Legacy Web UI      │         Modern API Clients           │
│  (Server Rendered)   │    (React/Vue/Mobile Apps)           │
└──────────┬───────────┴──────────────────┬───────────────────┘
           │                               │
           ▼                               ▼
┌──────────────────────────────────────────────────────────────┐
│                     Django Application                        │
├──────────────────────┬──────────────────────────────────────┤
│   Legacy Apps        │         API Apps (DRF)               │
│  - accounts          │    - apps.accounts                    │
│  - property          │    - apps.properties                  │
│  - leads             │    - apps.enquiries                   │
│  - payment           │    - apps.wishlist                    │
│                      │    - apps.dashboard                   │
└──────────┬───────────┴──────────────────┬───────────────────┘
           │                               │
           ▼                               ▼
┌──────────────────────────────────────────────────────────────┐
│                      Database Layer                           │
│                    (SQLite / MySQL)                           │
└──────────────────────────────────────────────────────────────┘
           │                               │
           ▼                               ▼
┌──────────────────────────────────────────────────────────────┐
│                   External Services                           │
│  - Razorpay (Payments)                                       │
│  - Google OAuth (Authentication)                             │
│  - SMTP (Email)                                              │
│  - OpenStreetMap (Maps)                                      │
└──────────────────────────────────────────────────────────────┘
```

### Application Flow

```
User Request
     │
     ├─→ Legacy UI Flow
     │   ├─→ Django Views (accounts, property, leads, payment)
     │   ├─→ Templates Rendering
     │   └─→ HTML Response
     │
     └─→ API Flow
         ├─→ DRF ViewSets (apps.*)
         ├─→ JWT Authentication
         ├─→ Serializers
         └─→ JSON Response
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- Virtual environment tool (venv/virtualenv)

### Installation (5 Minutes)

```bash
# 1. Clone the repository
git clone https://github.com/PANTH1101/real-estate-platform.git
cd real-estate-platform

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Navigate to project directory
cd real_estate

# 6. Run migrations
python manage.py migrate

# 7. Load initial data
python manage.py loaddata property/fixtures/initial_amenities.json

# 8. Create superuser
python manage.py createsuperuser

# 9. Run development server
python manage.py runserver
```

### Access the Application

- **Home**: http://127.0.0.1:8000/
- **Property Listings**: http://127.0.0.1:8000/properties/
- **Admin Panel**: http://127.0.0.1:8000/properties/admin/login/
- **Django Admin**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in `real_estate/` directory:

```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Leave empty for SQLite)
DB_ENGINE=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@realestatehub.com

# Razorpay (Get from https://razorpay.com/)
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret

# Google OAuth (Get from Google Cloud Console)
GOOGLE_OAUTH_CLIENT_ID=your_google_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_google_client_secret

# JWT Settings (Optional)
JWT_ACCESS_MINUTES=15
JWT_REFRESH_DAYS=7

# CORS Settings (Optional)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
CSRF_TRUSTED_ORIGINS=http://localhost:3000
```

### Database Configuration

#### SQLite (Default - Development)

No configuration needed. Database file will be created automatically as `db_core.sqlite3`.

#### MySQL (Production)

```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=real_estate_db
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

Install MySQL client:
```bash
pip install mysqlclient
```

### Email Configuration

#### Development (Console Backend)
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```
Emails will be printed to console.

#### Production (Gmail SMTP)
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=1
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
```

**Note**: For Gmail, you need to generate an [App Password](https://support.google.com/accounts/answer/185833).

---

## 📖 Usage

### For Buyers

#### 1. Browse Properties
```
Navigate to: /properties/
- Use filters to narrow down search
- Click on property cards for details
```

#### 2. View Property Details
```
- Login required to view full details
- See property specifications
- View location on interactive map
- Check amenities and features
```

#### 3. Contact Seller
```
- Click "Contact Seller" button
- Verify email with OTP
- Get seller contact information
```

### For Sellers

#### 1. Register/Login
```
Navigate to: /accounts/signup/
- Register as seller
- Or use Google OAuth
```

#### 2. List a Property
```
Navigate to: /property/create/
- Fill in property details
- Upload images (multiple)
- Select location on map
- Choose property type
- Add amenities
- Submit for approval
```

#### 3. Manage Properties
```
Navigate to: /accounts/dashboard/
- View all your listings
- Edit property details
- Check enquiries
- Monitor performance
```

### For Administrators

#### 1. Access Admin Panel
```
Navigate to: /properties/admin/login/
- View pending properties
- Approve/reject listings
- Monitor payments
- Manage amenities
```

#### 2. Django Admin
```
Navigate to: /admin/
- Full database access
- User management
- Advanced configurations
```

---

## 🔌 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication

#### Register
```http
POST /api/accounts/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe",
  "role": "BUYER"
}
```

#### Login
```http
POST /api/accounts/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```http
POST /api/accounts/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Properties

#### List Properties
```http
GET /api/properties/
Authorization: Bearer <access_token>

Query Parameters:
- property_type: APARTMENT, VILLA, PLOT, COMMERCIAL, SHOP
- min_price: number
- max_price: number
- bedrooms: number
- city: string
- is_active: boolean
- ordering: price, -price, created_at, -created_at
```

#### Get Property Details
```http
GET /api/properties/{id}/
Authorization: Bearer <access_token>
```

#### Create Property (Seller only)
```http
POST /api/properties/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

{
  "title": "Luxury Villa",
  "description": "Beautiful 3BHK villa",
  "property_type": "VILLA",
  "price": 5000000,
  "address": "123 Main St",
  "city": "Mumbai",
  "state": "Maharashtra",
  "pincode": "400001",
  "latitude": 19.0760,
  "longitude": 72.8777,
  "bedrooms": 3,
  "bathrooms": 2,
  "area": 2000,
  "images": [file1, file2, ...]
}
```

#### Update Property
```http
PUT /api/properties/{id}/
Authorization: Bearer <access_token>
```

#### Delete Property
```http
DELETE /api/properties/{id}/
Authorization: Bearer <access_token>
```

### Wishlist

#### Get Wishlist
```http
GET /api/wishlist/
Authorization: Bearer <access_token>
```

#### Add to Wishlist
```http
POST /api/wishlist/
Authorization: Bearer <access_token>

{
  "property": property_id
}
```

#### Remove from Wishlist
```http
DELETE /api/wishlist/{id}/
Authorization: Bearer <access_token>
```

### Enquiries

#### Create Enquiry
```http
POST /api/enquiries/
Authorization: Bearer <access_token>

{
  "property": property_id,
  "message": "I'm interested in this property"
}
```

#### List My Enquiries
```http
GET /api/enquiries/
Authorization: Bearer <access_token>
```

### Dashboard

#### Get Dashboard Stats
```http
GET /api/dashboard/stats/
Authorization: Bearer <access_token>

Response:
{
  "total_properties": 10,
  "active_properties": 8,
  "total_enquiries": 25,
  "pending_approvals": 2
}
```

---

## 📁 Project Structure

```
real-estate-platform/
│
├── real_estate/                    # Main Django project
│   ├── config/                     # Project configuration
│   │   ├── settings/
│   │   │   ├── base.py            # Base settings
│   │   │   ├── dev.py             # Development settings
│   │   │   └── prod.py            # Production settings
│   │   ├── urls.py                # Main URL configuration
│   │   ├── wsgi.py                # WSGI configuration
│   │   └── asgi.py                # ASGI configuration
│   │
│   ├── apps/                       # Modern API apps
│   │   ├── accounts/              # User authentication & profiles
│   │   ├── properties/            # Property management API
│   │   ├── wishlist/              # Wishlist functionality
│   │   ├── enquiries/             # Enquiry management
│   │   └── dashboard/             # Dashboard statistics
│   │
│   ├── accounts/                   # Legacy authentication
│   ├── property/                   # Legacy property management
│   ├── leads/                      # Lead verification system
│   ├── payment/                    # Payment processing
│   │
│   ├── templates/                  # HTML templates
│   │   ├── base.html              # Base template
│   │   ├── auth/                  # Authentication templates
│   │   ├── properties/            # Property templates
│   │   └── dashboard/             # Dashboard templates
│   │
│   ├── static/                     # Static files
│   │   ├── css/                   # Stylesheets
│   │   └── js/                    # JavaScript files
│   │
│   ├── media/                      # User uploads
│   │   └── property_images/       # Property images
│   │
│   ├── manage.py                   # Django management script
│   └── .env                        # Environment variables
│
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── README.txt                      # Original documentation
├── MAP_LOCATION_FEATURE.md        # Map feature documentation
├── LOCATION_SEARCH_GUIDE.md       # Location search guide
├── run_server.bat                  # Quick start script (Windows)
└── .gitignore                      # Git ignore rules
```

---

## 🗄️ Database Schema

### Core Models

#### User (apps.accounts.models.User)
```python
- id: UUID (Primary Key)
- email: EmailField (Unique)
- full_name: CharField
- phone_number: CharField
- role: CharField (BUYER/SELLER/ADMIN)
- is_email_verified: BooleanField
- is_active: BooleanField
- is_staff: BooleanField
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### Property (apps.properties.models.Property)
```python
- id: UUID (Primary Key)
- seller: ForeignKey(User)
- title: CharField
- description: TextField
- property_type: CharField
- price: DecimalField
- address: TextField
- city: CharField
- state: CharField
- pincode: CharField
- latitude: DecimalField (Optional)
- longitude: DecimalField (Optional)
- bedrooms: IntegerField
- bathrooms: IntegerField
- area: DecimalField
- is_active: BooleanField
- is_featured: BooleanField
- created_at: DateTimeField
- updated_at: DateTimeField
```

#### PropertyImage (apps.properties.models.PropertyImage)
```python
- id: UUID (Primary Key)
- property: ForeignKey(Property)
- image: ImageField
- is_primary: BooleanField
- uploaded_at: DateTimeField
```

#### Wishlist (apps.wishlist.models.Wishlist)
```python
- id: UUID (Primary Key)
- user: ForeignKey(User)
- property: ForeignKey(Property)
- created_at: DateTimeField
```

#### Enquiry (apps.enquiries.models.Enquiry)
```python
- id: UUID (Primary Key)
- property: ForeignKey(Property)
- buyer: ForeignKey(User)
- message: TextField
- status: CharField
- created_at: DateTimeField
```

### Relationships

```
User (Seller) ──1:N──> Property
User (Buyer) ──1:N──> Wishlist ──N:1──> Property
User (Buyer) ──1:N──> Enquiry ──N:1──> Property
Property ──1:N──> PropertyImage
Property ──N:N──> Amenity
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.properties

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Manual Testing Checklist

#### Authentication
- [ ] User registration
- [ ] Email verification
- [ ] Login/Logout
- [ ] Password reset
- [ ] Google OAuth login
- [ ] JWT token generation
- [ ] Token refresh

#### Property Management
- [ ] Create property listing
- [ ] Upload multiple images
- [ ] Select location on map
- [ ] Search location by address
- [ ] Edit property
- [ ] Delete property
- [ ] View property details
- [ ] Filter properties

#### Buyer Features
- [ ] Browse properties
- [ ] Add to wishlist
- [ ] Remove from wishlist
- [ ] Submit enquiry
- [ ] Email OTP verification
- [ ] View seller contact

#### Admin Features
- [ ] View pending properties
- [ ] Approve property
- [ ] Reject property
- [ ] View statistics
- [ ] Manage amenities
- [ ] User management

#### Payment
- [ ] Initiate payment
- [ ] Razorpay integration
- [ ] Payment success
- [ ] Payment failure
- [ ] Transaction tracking

---

## 🚢 Deployment

### Production Checklist

- [ ] Set `DJANGO_DEBUG=0`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use strong `SECRET_KEY`
- [ ] Set up MySQL database
- [ ] Configure production email backend
- [ ] Set up static file serving
- [ ] Configure media file storage
- [ ] Enable HTTPS
- [ ] Set up CORS properly
- [ ] Configure Razorpay production keys
- [ ] Set up backup strategy
- [ ] Configure logging
- [ ] Set up monitoring

### Deployment Options

#### 1. Traditional Server (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx mysql-server

# Clone and setup
git clone <repository>
cd real-estate-platform
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure database
sudo mysql
CREATE DATABASE real_estate_db;
CREATE USER 'realestate'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON real_estate_db.* TO 'realestate'@'localhost';

# Run migrations
cd real_estate
python manage.py migrate
python manage.py collectstatic

# Setup Gunicorn
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# Configure Nginx (reverse proxy)
# Setup systemd service for auto-start
```

#### 2. Docker

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY real_estate/ .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DJANGO_DEBUG=0
      - DB_ENGINE=django.db.backends.mysql
      - DB_HOST=db
    depends_on:
      - db
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: real_estate_db
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

#### 3. Cloud Platforms

- **Heroku**: Use Heroku Postgres, configure Procfile
- **AWS**: EC2 + RDS + S3 for media files
- **DigitalOcean**: App Platform or Droplet
- **Google Cloud**: App Engine or Compute Engine
- **Azure**: App Service

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### Getting Started

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write unit tests for new features
- Keep commits atomic and well-described

### Pull Request Process

1. Update README.md with details of changes if needed
2. Update documentation for new features
3. Ensure all tests pass
4. Request review from maintainers
5. Squash commits before merging

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Django** - The web framework for perfectionists with deadlines
- **Django REST Framework** - Powerful and flexible toolkit for building Web APIs
- **Leaflet.js** - Open-source JavaScript library for mobile-friendly interactive maps
- **OpenStreetMap** - Free, editable map of the world
- **Razorpay** - Payment gateway solution
- **Contributors** - Thanks to all contributors who helped build this project

---

## 📞 Support

### Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [Leaflet Documentation](https://leafletjs.com/)
- [Razorpay Documentation](https://razorpay.com/docs/)

### Project Documentation

- [MAP_LOCATION_FEATURE.md](MAP_LOCATION_FEATURE.md) - Map integration details
- [LOCATION_SEARCH_GUIDE.md](LOCATION_SEARCH_GUIDE.md) - Location search usage
- [README.txt](README.txt) - Original project documentation

### Get Help

- **Issues**: [GitHub Issues](https://github.com/PANTH1101/real-estate-platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/PANTH1101/real-estate-platform/discussions)
- **Email**: support@realestatehub.com

---

## 🗺️ Roadmap

### Version 2.0 (Planned)

- [ ] Advanced search with AI-powered recommendations
- [ ] Virtual property tours (360° images)
- [ ] Mobile applications (iOS/Android)
- [ ] Real-time chat between buyers and sellers
- [ ] Property comparison feature
- [ ] Mortgage calculator
- [ ] Neighborhood insights and analytics
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Progressive Web App (PWA)

### Version 2.1 (Future)

- [ ] Blockchain-based property verification
- [ ] AR/VR property viewing
- [ ] AI chatbot for customer support
- [ ] Advanced analytics dashboard
- [ ] Integration with property valuation APIs
- [ ] Social media integration
- [ ] Referral program
- [ ] Subscription plans for sellers

---

## 📊 Project Statistics

- **Total Commits**: 16
- **Contributors**: 3
- **Lines of Code**: ~10,000+
- **API Endpoints**: 20+
- **Models**: 15+
- **Development Time**: 1 month
- **Last Updated**: March 2026

---

## 👥 Team

### Core Contributors

- **PANTH1101** - Initial setup, map features, admin panel
- **Rudrakumar06** - Templates, payment integration, dynamic forms
- **Hetbhalodiya91** - Property listings, authentication, location search

---

<div align="center">

**Made with ❤️ by the RealEstateHub Team**

[⬆ Back to Top](#-real-estate-platform)

</div>
