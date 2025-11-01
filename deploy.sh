#!/bin/bash

# 🚗 Car Wash Management System - Quick Deployment Script
# This script automates the deployment process for production

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="carwash_management"
APP_USER="carwash"
APP_DIR="/home/$APP_USER/$APP_NAME"
DOMAIN="yourdomain.com"
DB_NAME="carwash_db"
DB_USER="carwash_user"

echo -e "${BLUE}🚀 Starting Car Wash Management System Deployment...${NC}"

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root for security reasons"
   exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git curl

# Create application user
if ! id "$APP_USER" &>/dev/null; then
    print_status "Creating application user: $APP_USER"
    sudo adduser --disabled-password --gecos "" $APP_USER
    sudo usermod -aG sudo $APP_USER
else
    print_warning "User $APP_USER already exists"
fi

# Setup PostgreSQL
print_status "Configuring PostgreSQL..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || print_warning "Database $DB_NAME might already exist"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$(openssl rand -base64 32)';" 2>/dev/null || print_warning "User $DB_USER might already exist"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;"

# Clone repository (if not already present)
if [ ! -d "$APP_DIR" ]; then
    print_status "Cloning repository..."
    sudo -u $APP_USER git clone <YOUR_REPOSITORY_URL> $APP_DIR
else
    print_warning "Application directory already exists, updating..."
    sudo -u $APP_USER git -C $APP_DIR pull
fi

# Setup Python virtual environment
print_status "Setting up Python virtual environment..."
sudo -u $APP_USER python3 -m venv $APP_DIR/venv
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt
sudo -u $APP_USER $APP_DIR/venv/bin/pip install gunicorn psycopg2-binary

# Create environment file
print_status "Creating environment configuration..."
sudo -u $APP_USER cp $APP_DIR/env.example $APP_DIR/.env

# Generate secret key
SECRET_KEY=$(sudo -u $APP_USER $APP_DIR/venv/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
sudo -u $APP_USER sed -i "s/your-very-long-random-secret-key-here-change-this-in-production/$SECRET_KEY/" $APP_DIR/.env

# Update domain in .env
sudo -u $APP_USER sed -i "s/yourdomain.com/$DOMAIN/" $APP_DIR/.env

# Run Django setup
print_status "Setting up Django application..."
sudo -u $APP_USER bash -c "cd $APP_DIR && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=carwash_management.settings_production && python manage.py makemigrations"
sudo -u $APP_USER bash -c "cd $APP_DIR && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=carwash_management.settings_production && python manage.py setup_initial_data"
sudo -u $APP_USER bash -c "cd $APP_DIR && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=carwash_management.settings_production && python manage.py migrate"

# Create static files directory
print_status "Setting up static files..."
sudo mkdir -p /var/www/$APP_NAME/static
sudo mkdir -p /var/www/$APP_NAME/media
sudo chown -R $APP_USER:www-data /var/www/$APP_NAME

# Collect static files
sudo -u $APP_USER bash -c "cd $APP_DIR && source venv/bin/activate && export DJANGO_SETTINGS_MODULE=carwash_management.settings_production && python manage.py collectstatic --noinput"

# Create Gunicorn service
print_status "Creating Gunicorn service..."
sudo tee /etc/systemd/system/$APP_NAME.service > /dev/null <<EOF
[Unit]
Description=Car Wash Management Gunicorn daemon
After=network.target

[Service]
User=$APP_USER
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/venv/bin"
Environment="DJANGO_SETTINGS_MODULE=carwash_management.settings_production"
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind unix:$APP_DIR/$APP_NAME.sock carwash_management.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
print_status "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/$APP_NAME > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # Static files
    location /static/ {
        alias /var/www/$APP_NAME/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /var/www/$APP_NAME/media/;
        expires 30d;
    }

    # Main application
    location / {
        proxy_pass http://unix:$APP_DIR/$APP_NAME.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Start and enable services
print_status "Starting services..."
sudo systemctl daemon-reload
sudo systemctl start $APP_NAME
sudo systemctl enable $APP_NAME
sudo systemctl restart nginx

# Configure firewall
print_status "Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Create backup script
print_status "Creating backup script..."
sudo -u $APP_USER tee $APP_DIR/backup.sh > /dev/null <<'EOF'
#!/bin/bash
BACKUP_DIR="/home/carwash/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="carwash_db"

mkdir -p $BACKUP_DIR

# Database backup
pg_dump $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Media files backup
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /var/www/carwash_management/media/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

sudo chmod +x $APP_DIR/backup.sh

# Setup cron jobs
print_status "Setting up cron jobs..."
sudo -u $APP_USER crontab -l 2>/dev/null | { cat; echo "0 2 * * * $APP_DIR/backup.sh"; } | sudo -u $APP_USER crontab -

# Create health check script
print_status "Creating health check script..."
sudo -u $APP_USER tee $APP_DIR/health_check.py > /dev/null <<'EOF'
#!/usr/bin/env python3
import requests
import sys

try:
    response = requests.get('http://localhost/accounts/login/', timeout=10)
    if response.status_code == 200:
        print("✅ Application is healthy")
        sys.exit(0)
    else:
        print(f"❌ Application returned status {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Health check failed: {e}")
    sys.exit(1)
EOF

sudo chmod +x $APP_DIR/health_check.py

# Final status check
print_status "Performing final checks..."
sleep 5

if sudo systemctl is-active --quiet $APP_NAME; then
    print_status "Gunicorn service is running"
else
    print_error "Gunicorn service failed to start"
    sudo systemctl status $APP_NAME
fi

if sudo systemctl is-active --quiet nginx; then
    print_status "Nginx service is running"
else
    print_error "Nginx service failed to start"
    sudo systemctl status nginx
fi

# Test application
if $APP_DIR/health_check.py; then
    print_status "Application health check passed"
else
    print_warning "Application health check failed - check logs"
fi

echo -e "${GREEN}"
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Deployment Summary:"
echo "   • Application: $APP_NAME"
echo "   • Domain: $DOMAIN"
echo "   • User: $APP_USER"
echo "   • Directory: $APP_DIR"
echo "   • Database: $DB_NAME"
echo ""
echo "🌐 Access your application at: http://$DOMAIN"
echo "👤 Default login: admin / admin123"
echo ""
echo "📁 Important files:"
echo "   • Environment: $APP_DIR/.env"
echo "   • Logs: sudo journalctl -u $APP_NAME -f"
echo "   • Nginx config: /etc/nginx/sites-available/$APP_NAME"
echo "   • Service: /etc/systemd/system/$APP_NAME.service"
echo ""
echo "🔧 Useful commands:"
echo "   • Restart app: sudo systemctl restart $APP_NAME"
echo "   • View logs: sudo journalctl -u $APP_NAME -f"
echo "   • Test config: sudo nginx -t"
echo "   • Backup: $APP_DIR/backup.sh"
echo ""
echo "🔐 Next steps:"
echo "   1. Update DNS to point $DOMAIN to this server"
echo "   2. Install SSL certificate: sudo certbot --nginx -d $DOMAIN"
echo "   3. Update .env file with production settings"
echo "   4. Test all functionality"
echo -e "${NC}"



