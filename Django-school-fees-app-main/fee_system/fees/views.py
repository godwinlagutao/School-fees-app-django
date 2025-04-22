from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Student, FeePayment, Clearance, FeeCategory
from .forms import StudentRegistrationForm  # We'll create this next
from .utils import generate_clearance_pdf
from django.http import HttpResponse

def home(request):
    return render(request, 'fees/home.html')

def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        student_form = StudentRegistrationForm(request.POST)

        print("User Form Errors:", user_form.errors)  # Debug
        print("Student Form Errors:", student_form.errors)
        
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            
            # Safely create clearance if it doesn't exist
            Clearance.objects.get_or_create(student=student)
            
            login(request, user)
            return redirect('dashboard')
    else:
        user_form = UserCreationForm()
        student_form = StudentRegistrationForm()
    
    return render(request, 'fees/register.html', {
        'user_form': user_form,
        'student_form': student_form
    })

@login_required
def dashboard(request):
    student = request.user.student
    clearance = student.clearance
    
    # Get all payments for this student
    payments = FeePayment.objects.filter(student=student).select_related('fee_category')
    
    # Check if all fees are paid
    required_categories = FeeCategory.objects.filter(is_required_for_clearance=True)
    paid_categories = payments.values_list('fee_category', flat=True)
    
    is_fully_cleared = set(required_categories.values_list('id', flat=True)).issubset(set(paid_categories))

    context = {
        'student': student,
        'clearance': clearance,
        'is_fully_cleared': is_fully_cleared,
        'payments': payments,  # This is what was missing!
        'pending_fees': required_categories.exclude(id__in=paid_categories)  # Optional bonus
    }
    return render(request, 'fees/dashboard.html', context)


@login_required
def download_clearance(request):
    student = request.user.student
    pdf_buffer = generate_clearance_pdf(student)
    
    if pdf_buffer:
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{student.student_id}_clearance.pdf"'
        return response
    else:
        messages.error(request, "You haven't paid all required fees yet")
        return redirect('dashboard')