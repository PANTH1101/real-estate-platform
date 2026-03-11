RealEstateHub - Project README
==============================

Overview
--------
RealEstateHub is a Django-based real estate platform with:
- A legacy server-rendered UI for buyers, sellers, and admins.
- A newer API-first backend under /api with JWT auth.
- Property listing, payments, and lead verification workflows.

It supports multiple property types (Apartment, Villa/House, Plot/Land,
Commercial Office, Shop) with type-specific fields shown on the property
detail page.

Tech Stack
----------
- Python (recommended 3.9+)
- Django
- Django REST Framework (DRF)
- SimpleJWT (JWT auth)
- django-filter
- django-cors-headers
- python-dotenv (loads .env)
- Pillow (ImageField support)
- Leaflet.js + OpenStreetMap (map picker and map view)
- Razorpay (legacy payment flow)

Project Layout (High Level)
---------------------------
- real_estate/config/         Django settings and URL routing
- real_estate/property/       Legacy property UI + models + forms
- real_estate/accounts/       Legacy seller/buyer auth flows
- real_estate/leads/          Buyer lead verification (OTP via email)
- real_estate/payment/        Legacy payment flow (Razorpay)
- real_estate/apps/           API-first apps (accounts/properties/etc.)
- real_estate/templates/      Shared templates
- real_estate/static/         CSS/JS assets
- real_estate/media/          Uploaded images

Core Features
-------------
Buyer flow (legacy UI):
- Browse properties: /properties/
- View property details (buyer login required)
- Request seller contact via email OTP verification

Seller flow (legacy UI):
- Create listing: /property/create/
- Upload images and set map location
- Preview own listing even if not active
- Manage listings from seller dashboard

Admin flow (legacy UI):
- Custom admin panel: /properties/admin/login/
- Approve or deactivate properties
- Add and delete amenities
- Delete properties from the admin panel
- Django admin: /admin/

Map and Location
----------------
- Sellers can select a location on a map when creating/editing a property.
- Property detail page shows a read-only map if coordinates exist.
- Details: MAP_LOCATION_FEATURE.md and LOCATION_SEARCH_GUIDE.md

Setup (Local Development)
-------------------------
1) Create and activate a virtual environment
2) Install dependencies
   - At minimum:
     pip install django djangorestframework djangorestframework-simplejwt
     pip install django-filter django-cors-headers python-dotenv pillow

3) Configure environment variables
   - The app loads .env from real_estate/.env if present
   - Do NOT commit real secrets. Use placeholders locally.

   Common variables:
   - DJANGO_SECRET_KEY
   - DJANGO_DEBUG (1 or 0)
   - DJANGO_ALLOWED_HOSTS (comma-separated)
   - DB_ENGINE (empty for SQLite, or django.db.backends.mysql)
   - DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT (for MySQL)
   - EMAIL_BACKEND, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS
   - EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL
   - RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET (legacy payments)
   - GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET (legacy login)

4) Run migrations
   - From real_estate/:
     python manage.py migrate

5) (Optional) Load initial amenities
   - python manage.py loaddata property/fixtures/initial_amenities.json

6) Create an admin user
   - python manage.py createsuperuser

7) Run the server
   - python manage.py runserver

URLs (Common)
-------------
- Home (legacy): /
- Property list (legacy): /properties/
- Property create (seller): /property/create/
- Admin panel (legacy): /properties/admin/login/
- Django admin: /admin/

API (New)
---------
Base prefix: /api/
Includes:
- Accounts auth and profile endpoints
- Properties endpoints with filtering
- Wishlist endpoints
- Enquiries endpoints
- Dashboard endpoints

Notes on Property Details
-------------------------
- Property detail page shows only fields relevant to the property type.
- For example:
  - Villa: built-up area, plot area, garden, parking
  - Plot: plot area/length/width, boundary wall, corner plot
  - Apartment: BHK, floor, total floors, area, lift

Known Assumptions
-----------------
- This README assumes Python 3.9+ and a local dev setup.
- If your environment differs, adjust accordingly.

