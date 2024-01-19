from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .forms import AppointmentForm, ContactForm, CommentForm
from .models import *
from django.http import JsonResponse
from django.core.mail import send_mail,BadHeaderError
from django.contrib import messages
from django.core.paginator import Paginator

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
    single_department = get_object_or_404(Department, slug=slug) if slug and 'department' in template_name else None
    single_post = get_object_or_404(Post, slug = slug) if slug and 'post' in template_name else None
    post = Post.objects.all()  # Initialize post variable
    
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            post = Post.objects.filter(title__contains = query)
        else:
            post = Post.objects.all()

    paginator = Paginator(post, 1)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
            
        
            
    if request.method == 'POST':
        appointment = AppointmentForm(request.POST)
        contact = ContactForm(data=request.POST)
        if appointment.is_valid():
            appointment.save()
            messages.success(request, 'Your appointment has been scheduled successfully!')
            print("Form is valid. Data saved successfully.")
            return redirect(redirect_name)  # Redirect to the specified page after form submission
        else:
            messages.error(request, 'Check your phone number or fill other fields!')
            print("Form errors:", appointment.errors)
        if contact.is_valid():
            email = contact.cleaned_data['email']
            name = contact.cleaned_data['name']
            subject = contact.cleaned_data['subject']
            message = f"Email:{email}, Name:{name}, sent you a message:{contact.cleaned_data['message']}"
            # contact.save()
            # print(email)
            messages.success(request, 'Your message was sent successfully')
            send_mail(
                    subject,
                    message,
                    email,
                    ["davidomisakin4good@gmail.com"],
                    fail_silently=False,
                )  
            
            contact = ContactForm() 
        else:
            print("Form errors:", contact.errors)   
            contact = ContactForm()
            appointment = AppointmentForm()     
    else:
        contact = ContactForm()
        appointment = AppointmentForm()
    
    context = {
        'appointment': appointment,
        'departments': department,
        'reviews': review,
        'single_department': single_department,
        'doctors': doctor,
        'cform': contact,
        'posts': post,
        'single_post': single_post,
        "page_obj": page_obj
    }
    
    return render(request, template_name, context)


# Your views
def home(request):
    return handle_form_submission(request, 'index.html', 'home')

def department(request):
    return handle_form_submission(request, 'departments.html','department')

def single_department(request,slug):
    return handle_form_submission(request, 'single-department.html','department',slug)

def doctors(request):
    return handle_form_submission(request, 'doctor.html', 'doctors')

def contact(request):
    return handle_form_submission(request, 'contact.html', 'contact')

def post(request):
    return handle_form_submission(request, 'blog.html', 'post')

def single_post(request, slug):
    return handle_form_submission(request, 'single-blog.html', 'single_blog', slug)

def single_blog(request, slug):
    posts = Post.objects.all()[:4]
    category = Category.objects.all()
    department = Department.objects.all()
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save() # to update the number of views
    comments = post.comments.filter(active=True)
    user_comment = None
    if request.method == 'POST':
        appointment = AppointmentForm(request.POST)
        comment = CommentForm(data=request.POST)
        
        if appointment.is_valid():
            appointment.save()
            print("Form is valid. Data saved successfully.")
            return redirect('blog')  # Redirect to the specified page after form submission
        else:
            print("Form errors:", appointment.errors)
            
        if comment.is_valid():
            #  Create Comment object but don't save to database yet
            user_comment = comment.save(commit=False)
            # Assign the current post to the comment
            user_comment.post = post
            # Save the comment to the database
            user_comment.save()
            print('Nice one')
            messages.success(request,'Comment added succesffully')
            return HttpResponseRedirect('' + post.slug)
    else:
        appointment = AppointmentForm()
        comment = CommentForm()
        
    context = {
        'appointment': appointment,
        'single_post' : post,
        'posts' : posts,
        'category': category,
        'comment':comment, 
        'comments':comments, 
        'user_comment':user_comment,
        'departments': department,
    }
        
    return render(request, 'single-blog.html', context)


def custom_404(request, exception):
    return render(request, '404.html', status=404)