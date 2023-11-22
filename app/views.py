from django.shortcuts import render, redirect, get_object_or_404
from .forms import AppointmentForm
from .models import *
from django.http import JsonResponse

# Create your views here.
# def home(request):
#     department = Department.objects.all()
#     if request.method =='POST':
#         appointment = AppointmentForm(request.POST)
#         if appointment.is_valid():
#             appointment.save()
#         else:
#             print('There was an error creating appointment')
#     else:
#           appointment = AppointmentForm()
#     return render(request, 'index.html',{'appointment':appointment,'department':department})
# def home(request):
#     department = Department.objects.all()
#     if request.method == 'POST':
#         appointment = AppointmentForm(request.POST)
#         if appointment.is_valid():
#             appointment.save()
#             print("Form is valid. Data saved successfully.")
#             return redirect('home')  # Redirect to the same page after form submission
#         else:
#             print("Form errors:", appointment.errors)
#     else:
#         appointment = AppointmentForm()
#     return render(request, 'index.html', {'appointment': appointment, 'department': department})


# def department(request):
#     if request.method == 'POST':
#         if appointment.is_valid():
#             appointment.save()
#             print("Form is valid. Data saved successfully.")
#             return redirect('home')  # Redirect to the same page after form submission
#         else:
#             print("Form errors:", appointment.errors)
#     else:
#         appointment = AppointmentForm()
#     return render(request, 'Department.html',{'appointment': appointment})

# def doctors(request):
#     if request.method == 'POST':
#         if appointment.is_valid():
#             appointment.save()
#             print("Form is valid. Data saved successfully.")
#             return redirect('home')  # Redirect to the same page after form submission
#         else:
#             print("Form errors:", appointment.errors)
#     else:
#         appointment = AppointmentForm()
#     return render(request, 'doctors.html',{'appointment': appointment})

# def contact(request):
#     if request.method == 'POST':
#         if appointment.is_valid():
#             appointment.save()
#             print("Form is valid. Data saved successfully.")
#             return redirect('home')  # Redirect to the same page after form submission
#         else:
#             print("Form errors:", appointment.errors)
#     else:
#         appointment = AppointmentForm()
#     return render(request, 'contact.html',{'appointment': appointment})


def handle_form_submission(request, template_name, redirect_name,slug=None):
    department = Department.objects.all()
    review = Review.objects.all()
    doctor = Doctor.objects.all()
    single_department = get_object_or_404(Department, slug = slug) if slug else None

    if request.method == 'POST':
        appointment = AppointmentForm(request.POST)
        if appointment.is_valid():
            appointment.save()
            print("Form is valid. Data saved successfully.")
            return redirect(redirect_name)  # Redirect to the specified page after form submission
        else:
            print("Form errors:", appointment.errors)
    else:
        appointment = AppointmentForm()
    
    context = {
        'appointment': appointment,
        'departments': department,
        'reviews': review,
        'single_department': single_department,
        'doctors': doctor
    }
    
    return render(request, template_name, context)


# Your views
def home(request):
    return handle_form_submission(request, 'index.html', 'home')

def department(request):
    return handle_form_submission(request, 'Department.html','department')

def single_department(request,slug):
    return handle_form_submission(request, 'single-department.html','department',slug)

def doctors(request):
    return handle_form_submission(request, 'doctors.html', 'doctors')

def contact(request):
    return handle_form_submission(request, 'contact.html', 'contact')