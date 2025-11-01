# 🚗 Car Wash Management System

A comprehensive Django-based web application for managing car wash operations with role-based access control, attendance tracking, and communication features.

## 🌟 Features

### 👥 User Roles
- **SuperAdmin**: Full system access and management
- **Author**: Manager role with instruction creation and employee oversight
- **Employer**: Employee role with attendance tracking and request submission

### 🎯 Core Functionality
- **Dashboard**: Role-specific dashboards with relevant information
- **Customer Management**: Complete customer database with service history
- **Service Management**: Multiple service types with pricing
- **Ticket System**: Service tickets with status tracking
- **Attendance Tracking**: Daily attendance with time tracking
- **Communication**: Request/reply system between roles
- **Instructions**: Author can create instructions for employees
- **Private Notes**: Secure messaging between Author and Employer
- **Reports**: Comprehensive reporting system

### 🛠️ Technical Features
- **Responsive Design**: Bootstrap 5 with mobile-friendly interface
- **Role-Based Access**: Secure access control with decorators
- **Database**: PostgreSQL (production) / SQLite (development)
- **Timezone**: Asia/Dhaka timezone support
- **Security**: CSRF protection, secure authentication
- **Pagination**: Efficient data loading for large datasets

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+ (or SQLite for development)
- Git

### Installation

1. **Clone the repository**
```bash
git clone <your-repository-url>
cd carwash_management
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup database**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py setup_initial_data
```

5. **Run development server**
```bash
python manage.py runserver
```

6. **Access the application**
- URL: `http://127.0.0.1:8000`
- Default login: `admin` / `admin123`

## 📁 Project Structure

```
carwash_management/
├── accounts/                 # User management and authentication
│   ├── models.py            # Custom User model with roles
│   ├── views.py             # Authentication and dashboard views
│   ├── forms.py             # Login and signup forms
│   └── urls.py              # Account-related URLs
├── carwash/                 # Core car wash functionality
│   ├── models.py            # Customer, Service, Ticket models
│   ├── views.py             # CRUD operations and business logic
│   ├── forms.py             # Customer and service forms
│   └── urls.py              # Car wash URLs
├── attendance/              # Attendance tracking
│   ├── models.py            # Attendance and notes models
│   ├── views.py             # Attendance management
│   ├── forms.py             # Attendance forms
│   └── urls.py              # Attendance URLs
├── requests/                # Communication system
│   ├── models.py            # Request and reply models
│   ├── views.py             # Request/reply handling
│   ├── forms.py             # Request forms
│   └── urls.py              # Request URLs
├── reports/                 # Reporting system
│   └── views.py             # Report generation
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── accounts/            # Authentication templates
│   ├── carwash/             # Car wash templates
│   ├── attendance/          # Attendance templates
│   └── requests/            # Request templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── requirements.txt         # Python dependencies
├── manage.py               # Django management script
└── carwash_management/     # Project settings
    ├── settings.py         # Development settings
    ├── urls.py             # Main URL configuration
    └── wsgi.py             # WSGI configuration
```

## 🔐 Default Accounts

After running `setup_initial_data`, you'll have these accounts:

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| SuperAdmin | admin | admin123 | Full system access |
| Author | author | jahed1234 | Manager role |
| Employer | employer | employer123 | Employee role |

## 🎨 User Interface

### Dashboard Features
- **Role-specific navigation** with relevant menu items
- **Quick stats** showing key metrics
- **Recent activity** with latest updates
- **Responsive design** that works on all devices

### Key Pages
- **Login/Signup**: Secure authentication with role selection
- **Customer Management**: Add, edit, and view customer information
- **Service Tickets**: Create and track service requests
- **Attendance**: Mark daily attendance with time tracking
- **Messages**: Communication between Author and Employer
- **Instructions**: Author can create instructions for employees
- **Notes**: Private messaging system

## 🛡️ Security Features

- **Role-based access control** with decorators
- **CSRF protection** on all forms
- **Secure password handling** with Django's built-in system
- **Session management** with proper logout functionality
- **Input validation** on all forms
- **SQL injection protection** through Django ORM

## 📊 Database Models

### Core Models
- **User**: Extended Django user with role field
- **Customer**: Customer information and contact details
- **ServiceType**: Available services with pricing
- **Ticket**: Service requests with status tracking
- **EmployerAttendance**: Daily attendance records
- **EmployerRequest**: Communication between roles
- **EmployerNote**: Private notes from Author to Employer

## 🔧 Configuration

### Environment Variables
Copy `env.example` to `.env` and configure:
- Database settings
- Secret key
- Debug mode
- Email configuration
- Static files paths

### Timezone
Default timezone is set to `Asia/Dhaka`. Change in settings if needed.

## 📱 Mobile Support

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- All modern browsers

## 🚀 Deployment

### Linux/Ubuntu
Use the provided `deploy.sh` script for automated deployment:
```bash
chmod +x deploy.sh
./deploy.sh
```

### Windows
Follow the `WINDOWS_DEPLOYMENT.md` guide for IIS deployment.

### Manual Deployment
See `DEPLOYMENT_INSTRUCTIONS.md` for detailed manual deployment steps.

## 🔍 API Endpoints

### Authentication
- `POST /accounts/login/` - User login
- `GET /accounts/logout/` - User logout
- `POST /accounts/signup/employer/` - Employer registration
- `POST /accounts/signup/author/` - Author registration

### Car Wash
- `GET /carwash/` - Service list
- `POST /carwash/create/` - Create new service
- `GET /carwash/customers/` - Customer list
- `POST /carwash/customers/create/` - Add customer

### Attendance
- `GET /attendance/` - Attendance list
- `POST /attendance/mark/` - Mark attendance

### Requests
- `GET /requests/` - Request list
- `POST /requests/create/` - Create request
- `POST /requests/reply/<id>/` - Reply to request

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

## 📈 Performance

### Optimization Features
- **Database indexing** on frequently queried fields
- **Pagination** for large datasets
- **Static file optimization** with proper caching
- **Efficient queries** using Django ORM best practices

### Monitoring
- **Health check endpoint** for monitoring
- **Logging configuration** for debugging
- **Error tracking** with detailed error pages

## 🔄 Backup & Recovery

### Automated Backup
The deployment includes automated backup scripts:
- **Database backup** (PostgreSQL dump)
- **Media files backup** (compressed archive)
- **Retention policy** (keeps 7 days of backups)

### Manual Backup
```bash
# Database backup
pg_dump carwash_db > backup.sql

# Media files backup
tar -czf media_backup.tar.gz media/
```

## 🆘 Support & Troubleshooting

### Common Issues
1. **Permission errors**: Check file permissions and ownership
2. **Database connection**: Verify database credentials and service status
3. **Static files**: Run `collectstatic` and check web server configuration
4. **Template errors**: Verify template paths and syntax

### Log Locations
- **Application logs**: `/var/log/carwash/` (Linux) or `C:\inetpub\logs\` (Windows)
- **Web server logs**: `/var/log/nginx/` (Nginx) or IIS logs (Windows)
- **Database logs**: PostgreSQL or SQL Server logs

### Getting Help
1. Check the troubleshooting section in deployment guides
2. Review application logs for error details
3. Verify configuration settings
4. Test with default accounts

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Contact

For support or questions:
- Create an issue in the repository
- Check the documentation
- Review the deployment guides

---

**🎉 Thank you for using Car Wash Management System!**

Built with ❤️ using Django, Bootstrap, and modern web technologies.
