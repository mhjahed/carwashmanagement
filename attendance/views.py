from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from .models import EmployerAttendance, EmployerNote
from .forms import AttendanceForm, EmployerNoteForm
from accounts.models import User


@login_required
def attendance_list(request):
    """List attendance records."""
    if request.user.is_employer():
        # Show own attendance
        attendance_records = EmployerAttendance.objects.filter(user=request.user).order_by('-date')
    elif request.user.is_author() or request.user.is_superadmin():
        # Show all attendance records
        attendance_records = EmployerAttendance.objects.all().order_by('-date')
    else:
        messages.error(request, 'You do not have permission to view attendance.')
        return redirect('accounts:dashboard')
    
    # Filter by month if provided
    month_filter = request.GET.get('month')
    if month_filter:
        try:
            year, month = month_filter.split('-')
            attendance_records = attendance_records.filter(date__year=year, date__month=month)
        except ValueError:
            pass
    
    # Pagination
    paginator = Paginator(attendance_records, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'month_filter': month_filter,
    }
    
    return render(request, 'attendance/attendance_list.html', context)


@login_required
def mark_attendance(request):
    """Mark attendance (employers only)."""
    if not request.user.is_employer():
        messages.error(request, 'Only employers can mark attendance.')
        return redirect('accounts:dashboard')
    
    today = timezone.now().date()
    
    # Check if attendance already marked for today
    existing_attendance = EmployerAttendance.objects.filter(
        user=request.user,
        date=today
    ).first()
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=existing_attendance)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.user = request.user
            attendance.date = today
            attendance.save()
            
            if existing_attendance:
                messages.success(request, 'Attendance updated successfully!')
            else:
                messages.success(request, 'Attendance marked successfully!')
            
            return redirect('attendance:attendance_list')
    else:
        form = AttendanceForm(instance=existing_attendance)
    
    context = {
        'form': form,
        'existing_attendance': existing_attendance,
        'today': today,
    }
    
    return render(request, 'attendance/mark_attendance.html', context)


@login_required
def notes_list(request):
    """List employer notes."""
    if request.user.is_employer():
        # Show notes for this employer
        notes = EmployerNote.objects.filter(employer=request.user).order_by('-created_at')
    elif request.user.is_author():
        # Show notes created by this author
        notes = EmployerNote.objects.filter(author=request.user).order_by('-created_at')
    elif request.user.is_superadmin():
        # Show all notes
        notes = EmployerNote.objects.all().order_by('-created_at')
    else:
        messages.error(request, 'You do not have permission to view notes.')
        return redirect('accounts:dashboard')
    
    # Pagination
    paginator = Paginator(notes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'attendance/notes_list.html', {'page_obj': page_obj})


@login_required
def note_create(request):
    """Create a new note (authors only)."""
    if not (request.user.is_author() or request.user.is_superadmin()):
        messages.error(request, 'Only authors can create notes.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = EmployerNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            messages.success(request, 'Note created successfully!')
            return redirect('attendance:notes_list')
    else:
        form = EmployerNoteForm()
    
    return render(request, 'attendance/note_form.html', {'form': form, 'title': 'Create Note'})
