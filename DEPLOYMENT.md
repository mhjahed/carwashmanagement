# 🚀 Deployment Guide

This guide will help you deploy the Car Wash Management System to various hosting platforms.

## 📋 Pre-deployment Checklist

- [ ] Update `SECRET_KEY` in production settings
- [ ] Set `DEBUG=False` for production
- [ ] Configure database (PostgreSQL recommended)
- [ ] Set up email configuration
- [ ] Configure static files serving
- [ ] Set up domain and SSL certificate

## 🌐 Deployment Options

### 1. Render (Recommended)

Render provides easy Django deployment with PostgreSQL.

#### Steps:

1. **Create a Render account** at [render.com](https://render.com)

2. **Create a new Web Service**:
   - Connect your GitHub repository
   - Choose "Web Service"
   - Select your repository

3. **Configure the service**:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn carwash_management.wsgi:application
   ```

4. **Set environment variables**:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DB_NAME=carwash_db
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_HOST=your-db-host
   DB_PORT=5432
   ```

5. **Create a PostgreSQL database**:
   - Go to "New" → "PostgreSQL"
   - Choose your plan
   - Note the connection details

6. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete

### 2. Railway

Railway offers simple deployment with automatic scaling.

#### Steps:

1. **Create a Railway account** at [railway.app](https://railway.app)

2. **Deploy from GitHub**:
   - Connect your repository
   - Railway will auto-detect Django

3. **Add PostgreSQL database**:
   - Go to "New" → "Database" → "PostgreSQL"
   - Railway will automatically set environment variables

4. **Set environment variables**:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   DJANGO_SETTINGS_MODULE=carwash_management.settings_production
   ```

5. **Deploy**:
   - Railway will automatically deploy on push

### 3. DigitalOcean App Platform

DigitalOcean provides full control with App Platform.

#### Steps:

1. **Create a DigitalOcean account** at [digitalocean.com](https://digitalocean.com)

2. **Create a new App**:
   - Connect your GitHub repository
   - Choose "Web Service"

3. **Configure the app**:
   ```yaml
   name: carwash-management
   services:
   - name: web
     source_dir: /
     github:
       repo: your-username/carwash-management
       branch: main
     run_command: gunicorn carwash_management.wsgi:application
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: SECRET_KEY
       value: your-secret-key-here
     - key: DEBUG
       value: "False"
     - key: DJANGO_SETTINGS_MODULE
       value: carwash_management.settings_production
   ```

4. **Add PostgreSQL database**:
   - Go to "Create" → "Database"
   - Choose PostgreSQL
   - Select your plan

5. **Deploy**:
   - Click "Create Resources"

### 4. Heroku

Heroku is a traditional Django hosting platform.

#### Steps:

1. **Install Heroku CLI** and create account

2. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL addon**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   heroku config:set DEBUG=False
   heroku config:set DJANGO_SETTINGS_MODULE=carwash_management.settings_production
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py setup_initial_data
   ```

## 🔧 Production Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Settings (PostgreSQL)
DB_NAME=carwash_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Email Settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

### Database Migration

After deployment, run migrations:

```bash
python manage.py migrate
python manage.py setup_initial_data
```

### Static Files

Static files are automatically handled by WhiteNoise in production settings.

### SSL Certificate

Most hosting platforms provide free SSL certificates. Enable HTTPS for security.

## 🔒 Security Considerations

1. **Change default passwords**:
   - Update admin password
   - Change default user passwords

2. **Environment variables**:
   - Never commit `.env` files
   - Use strong secret keys

3. **Database security**:
   - Use strong database passwords
   - Restrict database access

4. **HTTPS**:
   - Always use HTTPS in production
   - Set secure cookie flags

## 📊 Monitoring

### Logs

Monitor application logs for errors:

```bash
# Render
render logs

# Railway
railway logs

# Heroku
heroku logs --tail
```

### Performance

- Monitor database performance
- Set up error tracking (Sentry)
- Monitor response times

## 🚨 Troubleshooting

### Common Issues

1. **Static files not loading**:
   - Check WhiteNoise configuration
   - Verify static files collection

2. **Database connection errors**:
   - Check database credentials
   - Verify database is running

3. **Import errors**:
   - Check Python path
   - Verify all dependencies installed

4. **Permission errors**:
   - Check file permissions
   - Verify user permissions

### Debug Mode

For debugging, temporarily set:
```bash
DEBUG=True
```

**Remember to set it back to False in production!**

## 📈 Scaling

### Horizontal Scaling

- Use load balancers
- Scale database connections
- Use CDN for static files

### Vertical Scaling

- Increase server resources
- Optimize database queries
- Use caching (Redis)

## 🔄 Updates

### Deploying Updates

1. **Test locally**:
   ```bash
   python manage.py test
   ```

2. **Deploy to staging** (if available)

3. **Deploy to production**:
   ```bash
   git push origin main
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Restart services** (if needed)

## 📞 Support

For deployment issues:

1. Check platform documentation
2. Review application logs
3. Test locally first
4. Contact platform support

---

**Happy Deploying! 🚀**
