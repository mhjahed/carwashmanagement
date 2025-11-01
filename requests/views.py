from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from .models import EmployerRequest, RequestReply
from .forms import EmployerRequestForm, RequestReplyForm
from accounts.models import User


@login_required
def request_list(request):
    """List requests based on user role."""
    if request.user.is_employer():
        # Show employer's own requests
        requests = EmployerRequest.objects.filter(user=request.user).order_by('-created_at')
    elif request.user.is_author():
        # Show all employer requests
        requests = EmployerRequest.objects.filter(is_instruction=False).order_by('-created_at')
    else:
        messages.error(request, 'You do not have permission to view requests.')
        return redirect('accounts:dashboard')
    
    # Pagination
    paginator = Paginator(requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'requests/request_list.html', {'page_obj': page_obj})


@login_required
def request_create(request):
    """Create a new request or instruction."""
    if request.method == 'POST':
        form = EmployerRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.user = request.user
            
            # Check if this is an instruction (for authors)
            if request.user.is_author():
                request_obj.is_instruction = True
            
            request_obj.save()
            
            if request_obj.is_instruction:
                messages.success(request, 'Instruction created successfully!')
                return redirect('requests:instruction_list')
            else:
                messages.success(request, 'Request sent successfully!')
                return redirect('requests:request_list')
    else:
        form = EmployerRequestForm()
    
    # Determine title based on user role
    if request.user.is_author():
        title = 'Create Instruction'
    else:
        title = 'Send Request'
    
    return render(request, 'requests/request_form.html', {'form': form, 'title': title})


@login_required
def request_reply(request, request_id):
    """Reply to a request (authors only)."""
    if not request.user.is_author():
        messages.error(request, 'Only authors can reply to requests.')
        return redirect('accounts:dashboard')
    
    employer_request = get_object_or_404(EmployerRequest, id=request_id)
    
    if request.method == 'POST':
        form = RequestReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.request = employer_request
            reply.author = request.user
            reply.save()
            messages.success(request, 'Reply sent successfully!')
            return redirect('requests:request_list')
    else:
        form = RequestReplyForm()
    
    # Get all replies for this request
    replies = RequestReply.objects.filter(request=employer_request).order_by('created_at')
    
    context = {
        'employer_request': employer_request,
        'form': form,
        'replies': replies,
    }
    
    return render(request, 'requests/request_reply.html', context)


@login_required
def instruction_list(request):
    """List instructions (for employers) or manage instructions (for authors)."""
    if request.user.is_employer():
        # Show instructions for this employer
        instructions = EmployerRequest.objects.filter(
            user=request.user,
            is_instruction=True
        ).order_by('-created_at')
        
        # Pagination
        paginator = Paginator(instructions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'requests/instruction_list.html', {'page_obj': page_obj})
    
    elif request.user.is_author():
        # Show all instructions for management
        instructions = EmployerRequest.objects.filter(is_instruction=True).order_by('-created_at')
        
        # Pagination
        paginator = Paginator(instructions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'requests/instruction_manage.html', {'page_obj': page_obj})
    
    else:
        messages.error(request, 'You do not have permission to view instructions.')
        return redirect('accounts:dashboard')
