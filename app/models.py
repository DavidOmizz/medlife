from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from medilife.settings import EMAIL_HOST_USER
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Specialty(models.Model):
    name = models.CharField(max_length=255)
    decsciption = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Department(models.Model):
    image = models.ImageField(upload_to='department-images')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null= True, blank=True)
    description = RichTextField()


    def __str__(self):
        return self.name
    
class Review(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.name

class Doctor(models.Model):
    image = models.ImageField(upload_to='doctor-images')
    name = models.CharField(max_length=255)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    image = models.ImageField(upload_to='blog')
    title = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now= True)
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_post')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=300, unique=True)
    content = RichTextField()
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Appointment(models.Model):
    APPOINTMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )
    patient_name = models.CharField(max_length=255)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    number = models.CharField(max_length=15)
    patient_email = models.EmailField()
    status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS, default='Pending')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient_name
    
@receiver(post_save, sender=Appointment)
def send_approval_email(sender, instance, **kwargs):
        
    # Send an email to the doctor for approval
    from_email = EMAIL_HOST_USER
    doc_subject = 'You have an appointment'
    doc_message = f"An appointment has been received \n Patient name: {instance.patient_name} \n Patient email: {instance.patient_email} \n Date: {instance.appointment_date} \n Time: {instance.appointment_time} \n\n Kindly supply if you'll be available to move forward in the pipeline.\n\n\nCheers"
    doc_recipient_list = [instance.doctor.email]
    approved_doc_message = f"Hello {instance.doctor.name}, \n You have an approved appointment with {instance.patient_name}. \n Date: {instance.appointment_date} \n Time: {instance.appointment_time} \n\n Kindly be prepared ahead. Thanks  \n\n cheers"

    if instance.status == 'Pending':
        send_mail(doc_subject, doc_message, from_email, doc_recipient_list)

    # Send email to the doctor on the appointment

    if instance.status == 'Approved':
        # Send an email to the user
        subject = 'Appointment Approved'
        message = f'Your appointment with Dr. {instance.doctor.name} on {instance.appointment_date} at {instance.appointment_time} has been approved.'
        # from_email = EMAIL_HOST_USER
        recipient_list = [instance.patient_email]
        send_mail(subject, message, from_email, recipient_list)
        send_mail(doc_subject, approved_doc_message, from_email, doc_recipient_list)



# from django.db import models
# from django.core.mail import send_mail
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from yourproject.settings import EMAIL_HOST_USER  # Import your email settings from settings.py

# class Department(models.Model):
#     name = models.CharField(max_length=100)
#     # Other fields for the department

# class Doctor(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     # Other fields for the doctor

# class Appointment(models.Model):
#     APPOINTMENT_STATUS = (
#         ('Pending', 'Pending'),
#         ('Approved', 'Approved'),
#     )

#     date = models.DateField()
#     time = models.TimeField()
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     number = models.CharField(max_length=15)
#     email = models.EmailField()
#     status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS, default='Pending')

# @receiver(post_save, sender=Appointment)
# def send_approval_email(sender, instance, **kwargs):
#     if instance.status == 'Approved':
#         # Send an email to the user
#         subject = 'Appointment Approved'
#         message = f'Your appointment with Dr. {instance.doctor.name} on {instance.date} at {instance.time} has been approved.'
#         from_email = EMAIL_HOST_USER
#         recipient_list = [instance.email]

#         send_mail(subject, message, from_email, recipient_list)

