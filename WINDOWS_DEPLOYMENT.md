# 🚗 Car Wash Management System - Windows Deployment Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [IIS Deployment](#iis-deployment)
3. [Windows Service Setup](#windows-service-setup)
4. [Database Configuration](#database-configuration)
5. [Environment Setup](#environment-setup)
6. [Security Configuration](#security-configuration)
7. [Monitoring & Maintenance](#monitoring--maintenance)

---

## 🔧 Prerequisites

### System Requirements
- **Windows Server 2019/2022** or **Windows 10/11**
- **Python 3.8+** with pip
- **PostgreSQL 12+** or **SQL Server**
- **IIS 10+** with URL Rewrite module
- **Git** for version control

### Software Installation
```powershell
# Install Python (if not already installed)
# Download from: https://www.python.org/downloads/

# Install PostgreSQL
# Download from: https://www.postgresql.org/download/windows/

# Install IIS with required features
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole, IIS-WebServer, IIS-CommonHttpFeatures, IIS-HttpErrors, IIS-HttpLogging, IIS-RequestFiltering, IIS-StaticContent, IIS-DefaultDocument, IIS-DirectoryBrowsing, IIS-ASPNET45

# Install URL Rewrite module
# Download from: https://www.iis.net/downloads/microsoft/url-rewrite
```

---

## 🌐 IIS Deployment

### 1. Install Python and Dependencies
```powershell
# Create application directory
New-Item -ItemType Directory -Path "C:\inetpub\wwwroot\carwash" -Force

# Clone repository
git clone <your-repository-url> C:\inetpub\wwwroot\carwash

# Create virtual environment
cd C:\inetpub\wwwroot\carwash
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install wfastcgi
```

### 2. Configure wfastcgi
```powershell
# Install wfastcgi
wfastcgi-enable

# Note the output - you'll need the path for web.config
# Example output: "C:\inetpub\wwwroot\carwash\venv\Scripts\python.exe|C:\inetpub\wwwroot\carwash\venv\Lib\site-packages\wfastcgi.py"
```

### 3. Create web.config
Create `C:\inetpub\wwwroot\carwash\web.config`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <system.webServer>
    <handlers>
      <add name="Python FastCGI" 
           path="*" 
           verb="*" 
           modules="FastCgiModule" 
           scriptProcessor="C:\inetpub\wwwroot\carwash\venv\Scripts\python.exe|C:\inetpub\wwwroot\carwash\venv\Lib\site-packages\wfastcgi.py" 
           resourceType="Unspecified" />
    </handlers>
    
    <rewrite>
      <rules>
        <rule name="Static Files" stopProcessing="true">
          <match url="^(static/.*|media/.*|favicon\.ico|robots\.txt)$" />
          <action type="None" />
        </rule>
        
        <rule name="Django Application" stopProcessing="true">
          <match url=".*" />
          <action type="Rewrite" url="handler.fcgi/{R:0}" appendQueryString="true" />
        </rule>
      </rules>
    </rewrite>
    
    <staticContent>
      <mimeMap fileExtension=".json" mimeType="application/json" />
    </staticContent>
    
    <httpErrors errorMode="Detailed" />
  </system.webServer>
  
  <appSettings>
    <add key="WSGI_HANDLER" value="carwash_management.wsgi.application" />
    <add key="PYTHONPATH" value="C:\inetpub\wwwroot\carwash" />
    <add key="DJANGO_SETTINGS_MODULE" value="carwash_management.settings_production" />
  </appSettings>
</configuration>
```

### 4. Create handler.fcgi
Create `C:\inetpub\wwwroot\carwash\handler.fcgi`:
```python
#!/usr/bin/env python
import os
import sys

# Add the project directory to Python path
sys.path.insert(0, r'C:\inetpub\wwwroot\carwash')

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carwash_management.settings_production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5. Configure IIS Site
```powershell
# Create application pool
New-WebAppPool -Name "CarWashAppPool"
Set-ItemProperty -Path "IIS:\AppPools\CarWashAppPool" -Name "processModel.identityType" -Value "ApplicationPoolIdentity"
Set-ItemProperty -Path "IIS:\AppPools\CarWashAppPool" -Name "managedRuntimeVersion" -Value ""

# Create website
New-Website -Name "CarWash" -Port 80 -PhysicalPath "C:\inetpub\wwwroot\carwash" -ApplicationPool "CarWashAppPool"

# Set permissions
icacls "C:\inetpub\wwwroot\carwash" /grant "IIS_IUSRS:(OI)(CI)F" /T
icacls "C:\inetpub\wwwroot\carwash" /grant "IUSR:(OI)(CI)F" /T
```

---

## 🗄️ Database Configuration

### PostgreSQL Setup
```sql
-- Connect to PostgreSQL as superuser
-- Create database and user
CREATE DATABASE carwash_db;
CREATE USER carwash_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE carwash_db TO carwash_user;
ALTER USER carwash_user CREATEDB;
```

### SQL Server Setup (Alternative)
```sql
-- Connect to SQL Server
-- Create database
CREATE DATABASE carwash_db;

-- Create login and user
CREATE LOGIN carwash_user WITH PASSWORD = 'your_secure_password';
USE carwash_db;
CREATE USER carwash_user FOR LOGIN carwash_user;
ALTER ROLE db_owner ADD MEMBER carwash_user;
```

---

## ⚙️ Environment Setup

### 1. Create Production Settings
Create `carwash_management/settings_production.py`:
```python
from .settings import *
import os

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'localhost']

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
STATIC_ROOT = r'C:\inetpub\wwwroot\carwash\static'
MEDIA_ROOT = r'C:\inetpub\wwwroot\carwash\media'

# Security
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': r'C:\inetpub\logs\carwash.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 2. Set Environment Variables
```powershell
# Set environment variables
[Environment]::SetEnvironmentVariable("DB_NAME", "carwash_db", "Machine")
[Environment]::SetEnvironmentVariable("DB_USER", "carwash_user", "Machine")
[Environment]::SetEnvironmentVariable("DB_PASSWORD", "your_secure_password", "Machine")
[Environment]::SetEnvironmentVariable("SECRET_KEY", "your-secret-key", "Machine")
[Environment]::SetEnvironmentVariable("DJANGO_SETTINGS_MODULE", "carwash_management.settings_production", "Machine")

# Restart IIS to pick up environment variables
iisreset
```

### 3. Run Django Setup
```powershell
# Activate virtual environment
cd C:\inetpub\wwwroot\carwash
.\venv\Scripts\activate

# Set environment
$env:DJANGO_SETTINGS_MODULE = "carwash_management.settings_production"

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create initial data
python manage.py setup_initial_data

# Collect static files
python manage.py collectstatic --noinput
```

---

## 🔒 Security Configuration

### 1. Windows Firewall
```powershell
# Allow HTTP and HTTPS
New-NetFirewallRule -DisplayName "HTTP" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
New-NetFirewallRule -DisplayName "HTTPS" -Direction Inbound -Protocol TCP -LocalPort 443 -Action Allow
```

### 2. IIS Security
```powershell
# Disable directory browsing
Set-WebConfigurationProperty -Filter "system.webServer/directoryBrowse" -Name "enabled" -Value "False" -PSPath "IIS:\" -Location "CarWash"

# Set request filtering
Set-WebConfigurationProperty -Filter "system.webServer/security/requestFiltering" -Name "allowDoubleEscaping" -Value "False" -PSPath "IIS:\" -Location "CarWash"
```

### 3. SSL Certificate
```powershell
# Install SSL certificate (if you have one)
# Or use Let's Encrypt with win-acme
# Download from: https://github.com/win-acme/win-acme

# Configure HTTPS binding
New-WebBinding -Name "CarWash" -Protocol "https" -Port 443
```

---

## 📊 Monitoring & Maintenance

### 1. Windows Service (Alternative to IIS)
Create `carwash_service.py`:
```python
import win32serviceutil
import win32service
import win32event
import subprocess
import os

class CarWashService(win32serviceutil.ServiceFramework):
    _svc_name_ = "CarWashService"
    _svc_display_name_ = "Car Wash Management Service"
    _svc_description_ = "Django application for car wash management"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.process:
            self.process.terminate()
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        os.chdir(r'C:\inetpub\wwwroot\carwash')
        self.process = subprocess.Popen([
            r'C:\inetpub\wwwroot\carwash\venv\Scripts\python.exe',
            'manage.py', 'runserver', '0.0.0.0:8000'
        ])
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(CarWashService)
```

### 2. Install as Service
```powershell
# Install pywin32
pip install pywin32

# Install service
python carwash_service.py install

# Start service
python carwash_service.py start
```

### 3. Backup Script
Create `backup.ps1`:
```powershell
$BackupDir = "C:\Backups\CarWash"
$Date = Get-Date -Format "yyyyMMdd_HHmmss"
$DBName = "carwash_db"

# Create backup directory
New-Item -ItemType Directory -Path $BackupDir -Force

# Database backup (PostgreSQL)
& "C:\Program Files\PostgreSQL\13\bin\pg_dump.exe" -h localhost -U carwash_user -d $DBName -f "$BackupDir\db_backup_$Date.sql"

# Media files backup
Compress-Archive -Path "C:\inetpub\wwwroot\carwash\media\*" -DestinationPath "$BackupDir\media_backup_$Date.zip"

# Clean old backups (keep 7 days)
Get-ChildItem -Path $BackupDir -File | Where-Object {$_.CreationTime -lt (Get-Date).AddDays(-7)} | Remove-Item

Write-Host "Backup completed: $Date"
```

### 4. Task Scheduler
```powershell
# Create scheduled task for backup
$Action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\inetpub\wwwroot\carwash\backup.ps1"
$Trigger = New-ScheduledTaskTrigger -Daily -At 2AM
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings -TaskName "CarWashBackup" -Description "Daily backup for Car Wash Management System"
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Permission Errors
```powershell
# Fix IIS permissions
icacls "C:\inetpub\wwwroot\carwash" /grant "IIS_IUSRS:(OI)(CI)F" /T
icacls "C:\inetpub\wwwroot\carwash" /grant "IUSR:(OI)(CI)F" /T
```

#### 2. wfastcgi Issues
```powershell
# Reinstall wfastcgi
wfastcgi-disable
wfastcgi-enable
```

#### 3. Static Files Not Loading
```powershell
# Check static files configuration
python manage.py collectstatic --noinput --clear

# Verify IIS static content handler
Get-WebHandler -Name "StaticFile" -PSPath "IIS:\"
```

#### 4. Database Connection Issues
```powershell
# Test database connection
python manage.py dbshell

# Check PostgreSQL service
Get-Service postgresql*
```

### Log Locations
- **IIS Logs**: `C:\inetpub\logs\LogFiles\`
- **Application Logs**: `C:\inetpub\logs\carwash.log`
- **Windows Event Logs**: Event Viewer → Windows Logs → Application
- **Django Logs**: Check LOGGING configuration in settings

---

## 🚀 Quick Deployment Commands

```powershell
# Complete Windows deployment script
# Save as deploy_windows.ps1

Write-Host "🚀 Starting Car Wash Management System Deployment on Windows..." -ForegroundColor Blue

# Install IIS features
Enable-WindowsOptionalFeature -Online -FeatureName IIS-WebServerRole, IIS-WebServer, IIS-CommonHttpFeatures, IIS-HttpErrors, IIS-HttpLogging, IIS-RequestFiltering, IIS-StaticContent, IIS-DefaultDocument, IIS-DirectoryBrowsing, IIS-ASPNET45

# Create application directory
New-Item -ItemType Directory -Path "C:\inetpub\wwwroot\carwash" -Force

# Clone repository (update URL)
git clone <your-repository-url> C:\inetpub\wwwroot\carwash

# Setup Python environment
cd C:\inetpub\wwwroot\carwash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install wfastcgi

# Configure wfastcgi
wfastcgi-enable

# Set environment variables
[Environment]::SetEnvironmentVariable("DB_NAME", "carwash_db", "Machine")
[Environment]::SetEnvironmentVariable("DB_USER", "carwash_user", "Machine")
[Environment]::SetEnvironmentVariable("DB_PASSWORD", "your_secure_password", "Machine")
[Environment]::SetEnvironmentVariable("SECRET_KEY", "your-secret-key", "Machine")

# Run Django setup
$env:DJANGO_SETTINGS_MODULE = "carwash_management.settings_production"
python manage.py makemigrations
python manage.py migrate
python manage.py setup_initial_data
python manage.py collectstatic --noinput

# Configure IIS
New-WebAppPool -Name "CarWashAppPool"
Set-ItemProperty -Path "IIS:\AppPools\CarWashAppPool" -Name "managedRuntimeVersion" -Value ""
New-Website -Name "CarWash" -Port 80 -PhysicalPath "C:\inetpub\wwwroot\carwash" -ApplicationPool "CarWashAppPool"

# Set permissions
icacls "C:\inetpub\wwwroot\carwash" /grant "IIS_IUSRS:(OI)(CI)F" /T

# Restart IIS
iisreset

Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
Write-Host "🌐 Access your application at: http://localhost" -ForegroundColor Yellow
Write-Host "👤 Default login: admin / admin123" -ForegroundColor Yellow
```

---

**🎉 Your Car Wash Management System is now ready for Windows production!**

For any issues, check the troubleshooting section or Windows Event Viewer for detailed error messages.



