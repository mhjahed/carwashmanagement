from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .forms import EmployerSignupForm, AuthorSignupForm, UserLoginForm
from .models import User
from carwash.models import Ticket, ServiceType
from attendance.models import EmployerAttendance
from requests.models import EmployerRequest


def login_view(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def employer_signup(request):
    """Handle employer registration."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = EmployerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Employer account created successfully! Please login.')
            return redirect('accounts:login')
    else:
        form = EmployerSignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form, 'user_type': 'Employer'})


def author_signup(request):
    """Handle author registration."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = AuthorSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Author account created successfully! Please login.')
            return redirect('accounts:login')
    else:
        form = AuthorSignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form, 'user_type': 'Author'})


@login_required
def dashboard(request):
    """Main dashboard based on user role."""
    user = request.user
    today = timezone.now().date()
    
    if user.is_employer():
        return employer_dashboard(request, user, today)
    elif user.is_author():
        return author_dashboard(request, user, today)
    elif user.is_superadmin():
        return superadmin_dashboard(request, user, today)
    else:
        messages.error(request, 'Invalid user role.')
        return redirect('accounts:login')


def employer_dashboard(request, user, today):
    """Employer dashboard with progress and instructions."""
    # Get monthly progress
    current_month = today.replace(day=1)
    attendance_records = EmployerAttendance.objects.filter(
        user=user,
        date__gte=current_month
    )
    
    worked_days = attendance_records.filter(status='worked').count()
    missed_days = attendance_records.filter(status='missed').count()
    total_days = today.day
    
    # Get instructions and notes from Author
    instructions = EmployerRequest.objects.filter(
        user=user,
        is_instruction=True,
        is_active=True
    ).order_by('-created_at')[:5]
    
    # Get recent requests
    recent_requests = EmployerRequest.objects.filter(
        user=user,
        is_instruction=False
    ).order_by('-created_at')[:5]
    
    context = {
        'user': user,
        'today': today,
        'worked_days': worked_days,
        'missed_days': missed_days,
        'total_days': total_days,
        'instructions': instructions,
        'recent_requests': recent_requests,
    }
    
    return render(request, 'accounts/employer_dashboard.html', context)


def author_dashboard(request, user, today):
    """Author dashboard with events, tickets, and management tools."""
    # Get upcoming events (from SuperAdmin)
    # For now, we'll use a simple model - this can be enhanced later
    
    # Get ticket statistics
    total_tickets_today = Ticket.objects.filter(created_at__date=today).count()
    pending_tickets = Ticket.objects.filter(status='under_working').count()
    completed_tickets = Ticket.objects.filter(status='completed').count()
    
    # Get recent tickets
    recent_tickets = Ticket.objects.filter(status='under_working').order_by('-created_at')[:10]
    
    # Get employer requests
    employer_requests = EmployerRequest.objects.filter(
        is_instruction=False,
        is_active=True
    ).order_by('-created_at')[:10]
    
    context = {
        'user': user,
        'today': today,
        'total_tickets_today': total_tickets_today,
        'pending_tickets': pending_tickets,
        'completed_tickets': completed_tickets,
        'recent_tickets': recent_tickets,
        'employer_requests': employer_requests,
    }
    
    return render(request, 'accounts/author_dashboard.html', context)


def superadmin_dashboard(request, user, today):
    """SuperAdmin dashboard with system overview."""
    # Get system statistics
    total_users = User.objects.count()
    total_employers = User.objects.filter(role='employer').count()
    total_authors = User.objects.filter(role='author').count()
    
    # Get ticket statistics
    total_tickets = Ticket.objects.count()
    total_tickets_today = Ticket.objects.filter(created_at__date=today).count()
    
    # Get service types
    service_types = ServiceType.objects.all()
    
    context = {
        'user': user,
        'today': today,
        'total_users': total_users,
        'total_employers': total_employers,
        'total_authors': total_authors,
        'total_tickets': total_tickets,
        'total_tickets_today': total_tickets_today,
        'service_types': service_types,
    }
    
    return render(request, 'accounts/superadmin_dashboard.html', context)


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')  # <-- add namespace
