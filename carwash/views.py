from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from .models import ServiceType, Customer, Ticket
from .forms import CustomerForm, TicketForm, TicketUpdateForm
from accounts.models import User


@login_required
def ticket_list(request):
    """List all tickets with filtering and search."""
    if not (request.user.is_author or request.user.is_superadmin):
        messages.error(request, 'You do not have permission to view tickets.')
        return redirect('accounts:dashboard')
    
    tickets = Ticket.objects.all().order_by('-created_at')
    
    # Filtering
    status_filter = request.GET.get('status')
    payment_filter = request.GET.get('payment')
    service_filter = request.GET.get('service')
    search_query = request.GET.get('search')
    
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    
    if payment_filter:
        tickets = tickets.filter(payment_status=payment_filter)
    
    if service_filter:
        tickets = tickets.filter(service_type_id=service_filter)
    
    if search_query:
        tickets = tickets.filter(
            Q(ticket_id__icontains=search_query) |
            Q(car_number__icontains=search_query) |
            Q(customer__name__icontains=search_query) |
            Q(customer__phone__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(tickets, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    service_types = ServiceType.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'service_types': service_types,
        'current_filters': {
            'status': status_filter,
            'payment': payment_filter,
            'service': service_filter,
            'search': search_query,
        }
    }
    
    return render(request, 'carwash/ticket_list.html', context)


@login_required
def ticket_create(request):
    """Create a new ticket."""
    if not (request.user.is_author or request.user.is_superadmin):
        messages.error(request, 'You do not have permission to create tickets.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save()
            messages.success(request, f'Ticket {ticket.ticket_id} created successfully!')
            return redirect('carwash:ticket_preview', ticket_id=ticket.id)
    else:
        form = TicketForm()
    
    return render(request, 'carwash/ticket_form.html', {'form': form, 'title': 'Create New Ticket'})


@login_required
def ticket_preview(request, ticket_id):
    """Preview ticket before saving."""
    if not (request.user.is_author or request.user.is_superadmin):
        messages.error(request, 'You do not have permission to view tickets.')
        return redirect('accounts:dashboard')
    
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == 'POST':
        if 'confirm' in request.POST:
            messages.success(request, f'Ticket {ticket.ticket_id} confirmed and saved!')
            return redirect('carwash:ticket_list')
        elif 'edit' in request.POST:
            return redirect('carwash:ticket_update', ticket_id=ticket.id)
    
    return render(request, 'carwash/ticket_preview.html', {'ticket': ticket})


@login_required
def ticket_update(request, ticket_id):
    """Update ticket status and payment."""
    if not (request.user.is_author or request.user.is_superadmin):
        messages.error(request, 'You do not have permission to update tickets.')
        return redirect('accounts:dashboard')
    
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ticket {ticket.ticket_id} updated successfully!')
            return redirect('carwash:ticket_list')
    else:
        form = TicketUpdateForm(instance=ticket)
    
    return render(request, 'carwash/ticket_update.html', {'form': form, 'ticket': ticket})


@login_required
def customer_list(request):
    """List all customers with search."""
    if not (request.user.is_author or request.user.is_superadmin):
        messages.error(request, 'You do not have permission to view customers.')
        return redirect('accounts:dashboard')
    
    customers = Customer.objects.all().order_by('name')
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'carwash/customer_list.html', context)


@login_required
def customer_create(request):
    """Create a new customer."""
    if not (request.user.is_author or request.user.is_superadmin):
        messages.error(request, 'You do not have permission to create customers.')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer {customer.name} created successfully!')
            return redirect('carwash:customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'carwash/customer_form.html', {'form': form, 'title': 'Create New Customer'})


@login_required
def customer_update(request, customer_id):
    """Update customer information."""
    if not (request.user.is_author or request.user.is_superadmin):
        messages.error(request, 'You do not have permission to update customers.')
        return redirect('accounts:dashboard')
    
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer {customer.name} updated successfully!')
            return redirect('carwash:customer_list')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'carwash/customer_form.html', {'form': form, 'title': 'Update Customer', 'customer': customer})


@login_required
def get_service_price(request):
    """AJAX endpoint to get service price."""
    if not (request.user.is_author or request.user.is_superadmin):
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    service_id = request.GET.get('service_id')
    try:
        service = ServiceType.objects.get(id=service_id, is_active=True)
        return JsonResponse({'price': float(service.price)})
    except ServiceType.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)
