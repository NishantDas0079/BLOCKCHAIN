# 🚀 Blockchain Explorer - Django Web Application
# 📋 Overview
A Django-based web application for exploring blockchain data, visualizing transactions, and interacting with blockchain networks through a user-friendly interface.

# ✨ Features

🔍 Blockchain Data Explorer: Browse blocks, transactions, and addresses

📊 Real-time Visualization: Interactive charts and statistics

🔐 Admin Dashboard: Comprehensive management interface

📱 Responsive Design: Works on desktop and mobile devices

⚡ REST API: Programmatic access to blockchain data

# Backend
Django 4.2.0 - Web framework

Python 3.11+ - Programming language (recommended for compatibility)

crispy-bootstrap5 - Form styling with Bootstrap 5

python-decouple - Environment configuration

Pillow - Image processing (optional)

# Frontend
Bootstrap 5 - CSS framework

JavaScript - Interactive components

Chart.js - Data visualization

# Database
SQLite (default) or PostgreSQL for production

# Installation Steps
# 1. Clone the Repository
```
git clone <repository-url>
cd blockchain-explorer
```

# 2. Create virtual environment
```
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

# 3. Install dependencies
```
pip install Django==4.2.0 crispy-bootstrap5 python-decouple
# If needed, install Pillow with:
pip install Pillow==10.0.0 --no-binary Pillow
```

# 4. Set up environment variables
```
# Copy example environment file
cp .env.example .env
# Or create your own
echo "SECRET_KEY=your-secret-key-here" > .env
echo "DEBUG=True" >> .env
```

# 5. Run database migrations
```
python manage.py migrate
```

# 6. Create Superuser (admin)
```
python manage.py createsuperuser
```

# 7. Start development server
```
python manage.py runserver
```

# 8. Access the application
```
Main Site: http://127.0.0.1:8000/

Admin Panel: http://127.0.0.1:8000/admin/
```

# If your project includes a REST API:
```
# List available API endpoints
python manage.py show_urls

# Test API with curl
curl http://127.0.0.1:8000/api/blocks/
curl http://127.0.0.1:8000/api/transactions/
```

# Development commands
```
# Run tests
python manage.py test

# Check for code issues
python manage.py check

# Create new app
python manage.py startapp app_name

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

# 🌐 Deployment
# Production Checklist

Set DEBUG = False in .env

Update ALLOWED_HOSTS with your domain

Use PostgreSQL instead of SQLite

Configure static files with WhiteNoise or CDN

Set up Gunicorn/Uvicorn and Nginx

Configure HTTPS with SSL certificate

# Docker deployment (optional)
```
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "blockchain_explorer.wsgi:application", "--bind", "0.0.0.0:8000"]
```
