# 🚗 Car Wash Management System - Deployment Instructions

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Database Configuration](#database-configuration)
5. [Environment Variables](#environment-variables)
6. [Static Files & Media](#static-files--media)
7. [Security Configuration](#security-configuration)
8. [Web Server Configuration](#web-server-configuration)
9. [SSL/HTTPS Setup](#sslhttps-setup)
10. [Monitoring & Maintenance](#monitoring--maintenance)
11. [Backup Strategy](#backup-strategy)
12. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Database**: PostgreSQL 12+ (recommended) or SQLite (development)
- **Web Server**: Nginx (recommended) or Apache
- **WSGI Server**: Gunicorn or uWSGI
- **OS**: Linux (Ubuntu 20.04+ recommended) or Windows Server

### Software Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib nginx git

# CentOS/RHEL
sudo yum install python3 python3-pip postgresql-server postgresql-contrib nginx git
```

---

## 🏠 Local Development Setup

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repository-url>
cd carwash_management

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env
```

### 3. Database Setup
```bash
# Create database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser and initial data
python manage.py setup_initial_data
```

### 4. Run Development Server
```bash
python manage.py runserver 0.0.0.0:8000
```

---

## 🚀 Production Deployment

### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Create deployment user
sudo adduser carwash
sudo usermod -aG sudo carwash
su - carwash
```

### 2. Application Setup
```bash
# Clone repository
git clone <your-repository-url>
cd carwash_management

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 3. Production Settings
Create `carwash_management/settings_production.py`:
```python
from .settings import *
import os

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-server-ip']

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'carwash_db'),
        'USER': os.environ.get('DB_USER', 'carwash_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Static files
STATIC_ROOT = '/var/www/carwash/static/'
MEDIA_ROOT = '/var/www/carwash/media/'

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS settings (uncomment when SSL is configured)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
```

---

## 🗄️ Database Configuration

### PostgreSQL Setup
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
```

```sql
-- In PostgreSQL shell
CREATE DATABASE carwash_db;
CREATE USER carwash_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE carwash_db TO carwash_user;
ALTER USER carwash_user CREATEDB;
\q
```

### Database Migration
```bash
# Set environment variable
export DJANGO_SETTINGS_MODULE=carwash_management.settings_production

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create initial data
python manage.py setup_initial_data
```

---

## 🔐 Environment Variables

Create `.env` file:
```bash
# Database
DB_NAME=carwash_db
DB_USER=carwash_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Django
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Timezone
TIME_ZONE=Asia/Dhaka
```

---

## 📁 Static Files & Media

### Collect Static Files
```bash
# Create directories
sudo mkdir -p /var/www/carwash/static
sudo mkdir -p /var/www/carwash/media
sudo chown -R carwash:carwash /var/www/carwash

# Collect static files
python manage.py collectstatic --noinput
```

### Nginx Configuration
Create `/etc/nginx/sites-available/carwash`:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Static files
    location /static/ {
        alias /var/www/carwash/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/carwash/media/;
        expires 30d;
    }

    # Main application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/carwash /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔒 Security Configuration

### Firewall Setup
```bash
# UFW (Ubuntu)
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable

# Or iptables
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

### File Permissions
```bash
# Set proper permissions
chmod 755 /var/www/carwash
chmod 644 /var/www/carwash/static/*
chmod 644 /var/www/carwash/media/*
```

---

## 🌐 Web Server Configuration

### Gunicorn Setup
Create `/etc/systemd/system/carwash.service`:
```ini
[Unit]
Description=Car Wash Management Gunicorn daemon
After=network.target

[Service]
User=carwash
Group=www-data
WorkingDirectory=/home/carwash/carwash_management
Environment="PATH=/home/carwash/carwash_management/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=carwash_management.settings_production"
ExecStart=/home/carwash/carwash_management/venv/bin/gunicorn --workers 3 --bind unix:/home/carwash/carwash_management/carwash.sock carwash_management.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl daemon-reload
sudo systemctl start carwash
sudo systemctl enable carwash
```

### Update Nginx for Socket
Update nginx configuration:
```nginx
location / {
    proxy_pass http://unix:/home/carwash/carwash_management/carwash.sock;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

## 🔐 SSL/HTTPS Setup

### Let's Encrypt (Certbot)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Update Production Settings
Uncomment SSL settings in `settings_production.py`:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 📊 Monitoring & Maintenance

### Log Configuration
```bash
# Create log directory
sudo mkdir -p /var/log/carwash
sudo chown carwash:carwash /var/log/carwash

# Update Gunicorn service for logging
# Add to [Service] section:
StandardOutput=append:/var/log/carwash/gunicorn.log
StandardError=append:/var/log/carwash/gunicorn_error.log
```

### Health Check Script
Create `health_check.py`:
```python
#!/usr/bin/env python3
import requests
import sys

try:
    response = requests.get('http://localhost:8000/accounts/login/', timeout=10)
    if response.status_code == 200:
        print("✅ Application is healthy")
        sys.exit(0)
    else:
        print(f"❌ Application returned status {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Health check failed: {e}")
    sys.exit(1)
```

### Cron Jobs
```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /home/carwash/backup_script.sh

# Health check every 5 minutes
*/5 * * * * /home/carwash/carwash_management/health_check.py

# Log rotation
0 0 * * 0 /usr/sbin/logrotate /etc/logrotate.d/carwash
```

---

## 💾 Backup Strategy

### Database Backup Script
Create `backup_script.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/home/carwash/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="carwash_db"

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
pg_dump $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /var/www/carwash/media/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
```

```bash
# Make executable
chmod +x backup_script.sh
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Permission Errors
```bash
# Fix ownership
sudo chown -R carwash:www-data /var/www/carwash
sudo chmod -R 755 /var/www/carwash
```

#### 2. Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U carwash_user -d carwash_db
```

#### 3. Static Files Not Loading
```bash
# Recollect static files
python manage.py collectstatic --noinput --clear

# Check nginx configuration
sudo nginx -t
sudo systemctl reload nginx
```

#### 4. Gunicorn Not Starting
```bash
# Check service status
sudo systemctl status carwash

# Check logs
sudo journalctl -u carwash -f

# Test gunicorn manually
cd /home/carwash/carwash_management
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 carwash_management.wsgi:application
```

### Log Locations
- **Application logs**: `/var/log/carwash/`
- **Nginx logs**: `/var/log/nginx/`
- **System logs**: `/var/log/syslog`
- **Gunicorn logs**: `sudo journalctl -u carwash`

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks
1. **Weekly**: Check logs for errors
2. **Monthly**: Update system packages
3. **Quarterly**: Review and rotate logs
4. **Annually**: Security audit and dependency updates

### Performance Optimization
1. **Database**: Regular VACUUM and ANALYZE
2. **Static Files**: Use CDN for better performance
3. **Caching**: Implement Redis for session storage
4. **Monitoring**: Set up application monitoring (Sentry, New Relic)

---

## 🎯 Deployment Checklist

- [ ] Server prepared with required software
- [ ] Database created and configured
- [ ] Environment variables set
- [ ] Application deployed and tested
- [ ] Static files collected
- [ ] Web server configured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Backup strategy implemented
- [ ] Monitoring set up
- [ ] Health checks working
- [ ] Documentation updated

---

## 🚀 Quick Deployment Commands

```bash
# Complete deployment script
#!/bin/bash
set -e

echo "🚀 Starting Car Wash Management System Deployment..."

# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git

# 3. Setup database
sudo -u postgres createdb carwash_db
sudo -u postgres createuser carwash_user

# 4. Deploy application
git clone <your-repo> /home/carwash/carwash_management
cd /home/carwash/carwash_management
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# 5. Configure and start services
python manage.py migrate
python manage.py setup_initial_data
python manage.py collectstatic --noinput

# 6. Start services
sudo systemctl start carwash
sudo systemctl enable carwash
sudo systemctl restart nginx

echo "✅ Deployment completed successfully!"
echo "🌐 Visit: http://yourdomain.com"
echo "👤 Login: admin / admin123"
```

---

**🎉 Congratulations! Your Car Wash Management System is now ready for production!**

For any issues or questions, please refer to the troubleshooting section or contact your system administrator.



