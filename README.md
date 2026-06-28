# Backend Farmer App API

Django REST API backend for AgroMart/Farmer marketplace workflows.

## Overview

This backend provides:
- User authentication and profile management (custom user model + JWT)
- Password reset via email
- Contact form submission endpoint
- Farmer product management
- Buyer shopping flows (browse, cart, order, order history)
- Basic chatbot/help endpoint
- Cloudinary-based media storage

## Tech Stack

- Python
- Django 6
- Django REST Framework
- JWT auth via djangorestframework-simplejwt
- SQLite (local default)
- Cloudinary (media storage)
- WhiteNoise (static files)
- Gunicorn (deployment)

## Project Structure

- backend/manage.py: Django entrypoint
- backend/backend/settings.py: Main configuration
- backend/backend/urls.py: Root URL routing
- backend/AuthApp: Authentication and user management
- backend/ContactApp: Contact form API
- backend/FarmerApp: Products, cart, orders, earnings
- backend/Chatboat: Chat/help API
- backend/build.sh: Build script used for deployment
- backend/Procfile: Gunicorn process declaration

## Prerequisites

- Python 3.10+
- pip
- Virtual environment tool (venv)

## Local Setup

1. Open terminal in backend folder.
2. Create and activate virtual environment.
3. Install dependencies.
4. Run migrations.
5. Start development server.

### Windows (PowerShell)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Server runs at:
- http://127.0.0.1:8000/


## Authentication

JWT is enabled globally for DRF.

Token endpoints:
- POST /api/token/
- POST /api/token/refresh/

Also available custom login endpoint:
- POST /api/user/login/

## API Routes

### AuthApp (/api/user/)
- POST register/
- POST login/
- GET profile/<user_id>/
- POST forgot-password/
- POST reset-password/<uid>/<token>/

### ContactApp (/api/contactapp/)
- POST contact/

### FarmerApp (/api/farmer/)

Farmer product management:
- POST addproduct/
- PUT editproduct/<id>/
- DELETE deleteproduct/<id>/
- GET myproduct/

Buyer product browsing:
- GET allproducts/
- GET product/<product_id>/
- GET visitstore/<farmer_id>/

Cart:
- POST add-to-cart/
- GET view-cart/
- PUT update-cart/<item_id>/
- DELETE remove-cart/<item_id>/

Orders:
- POST buy-now/
- POST create-order/
- GET orders/<order_id>/
- GET myorders/
- GET orders/
- PATCH order-item/<item_id>/deliver/

Insights:
- GET earning/
- GET topbuyers/

### Chatboat (/api/ai/)
- POST chatboat/

## Data Notes

- Custom user model is AuthApp.User (email-based login)
- Local database defaults to SQLite (db.sqlite3)
- Product images and avatars are stored through Cloudinary

## Deployment Notes

This project includes deployment helpers:

- build.sh
  - pip install -r requirements.txt
  - python manage.py collectstatic --noinput
  - python manage.py migrate

- Procfile
  - web: gunicorn backend.wsgi

If deploying to Render or similar PaaS:
- Set all required environment variables
- Ensure static collection runs during build
- Ensure migrations run on deploy

## CORS

Currently allowed origins in settings:
- http://localhost:5173
- https://agromart-ad69.onrender.com

Update CORS_ALLOWED_ORIGINS in backend/backend/settings.py for your frontend domains.

## Useful Commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
python manage.py test
```

## Current Admin URL

- /admin/

## License

Copyright (c) 2026 Devkaran Patidar.

