from django.db import models
from django.core.mail import send_mail, EmailMessage
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
    appointment_date = models.DateField(blank=True, null = True)
    appointment_time = models.TimeField(blank=True, null = True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    number = models.CharField(max_length=15)
    patient_email = models.EmailField()
    status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS, default='Pending')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient_name
    
@receiver(post_save, sender=Appointment)
def send_approval_email(sender, instance, **kwargs):
    sender_name='Medilife Hospital'
    patient_name = instance.patient_name
    patient_email = instance.patient_email
    doctor_name = instance.doctor.name

    # Send an email to the doctor for approval
    from_email = EMAIL_HOST_USER
    hos_subject = 'Appointment Request Received'
    # hos_message = f"An appointment has been received \n Patient name: {instance.patient_name} \n Patient email: {instance.patient_email} \n\n Kindly supply attend to it.\n\n\nCheers"
    hos_message = (
        f"Dear Hospital/Administrator, \n\n"
        f"We are writing to inform you that a new appointment request has been received through our system. Below are the details:\n\n"
        f"- Patient Name: {patient_name}\n"
        f"- Patient Email: {patient_email}\n\n"
        f"We kindly request your attention to this appointment request at your earliest convenience. Your prompt action in attending to this matter would be greatly appreciated.\n\n"
        f"Should you require any further information or assistance, please do not hesitate to contact us.\n"
        f"Thank you for your attention to this matter.\n\n"
        f"Best regards,\n"
        f"Medilife"
    )
    hos_recipient_list = [from_email]
    
    doc_subject = 'New Appointment Request Notification'
    doc_message = (
        f'Dear {doctor_name},\n\n'
        f'We trust this message finds you well.\n\n'
        f'We wish to inform you that a new appointment request has been submitted by a patient. The details are as follows:\n\n'
        f'- Patient Name: {patient_name}\n'
        f'- Patient Email: {patient_email}\n\n'
        f'Your attention to this matter is kindly requested to confirm your availability and proceed accordingly.\n'
        f'Should you have any questions or require further information, please feel free to reach out to us.\n\n'
        f'Thank you for your prompt attention to this appointment request.\n\n'
        f"Best regards,\n"
        f"Medilife" 
    )
    # doc_message = f"An appointment has been received \n Patient name: {instance.patient_name} \n Patient email: {instance.patient_email} \n Date: {instance.appointment_date} \n Time: {instance.appointment_time} \n\n Kindly supply if you'll be available to move forward in the pipeline.\n\n\nCheers"
    doc_recipient_list = [instance.doctor.email]
    # approved_doc_message = f"Hello {instance.doctor.name}, \n You have an approved appointment with {instance.patient_name}. \n Date: {instance.appointment_date} \n Time: {instance.appointment_time} \n\n Kindly be prepared ahead. Thanks  \n\n cheers"
    approved_doc_subjects = 'Appointment Confirmation'
    approved_doc_message =(
        f'Hello {doctor_name},\n\n'
        f'We hope this message finds you well.\n'
        f'We are pleased to inform you that your appointment with {patient_name} has been approved.\n'
        f'Please make the necessary arrangements and be prepared for the scheduled appointment.\n\n'
        f'Thank you for your attention to this matter.\n\n'
        f"Best regards,\n"
        f"Medilife"
        # f"Hello {instance.doctor.name}, \n You have an approved appointment with {instance.patient_name}.\n\n Kindly be prepared ahead. Thanks  \n\n cheers"
    )

    if instance.status == 'Pending':
        #TO SEND MAIL WITH THE COMPANY NAME HEADER AS THE SENDER
        # send_mail(hos_subject, hos_message, from_email, hos_recipient_list)
        hos_email = EmailMessage(
            subject=hos_subject,
            body=hos_message,
            from_email='Medilife Hospital <noreply@example.com>',
            to=hos_recipient_list
        )
        hos_email.send()
        
        #TO SEND MAIL WITH THE COMPANY NAME HEADER AS THE SENDER
        # send_mail(doc_subject, doc_message, from_email, doc_recipient_list)
        doc_email = EmailMessage(
            subject=doc_subject,
            body=doc_message,
            from_email='Medilife Hospital <noreply@example.com>',
            to=doc_recipient_list
        )
        doc_email.send()

    if instance.status == 'Approved':
        subject = 'Appointment Confirmation'
        recipient_email = instance.patient_email  # Assuming you have the patient's email stored in the instance
        recipient_name = instance.patient_name  # Assuming you have the patient's name stored in the instance
        doctor_name = instance.doctor.name
        
        # Check if appointment_date is not None before formatting
            # appointment_date = instance.appointment_date.strftime('%Y-%m-%d')  # Format the date as desired
        if instance.appointment_date:
            appointment_date = instance.appointment_date.strftime('%Y-%m-%d')  # Format the date as desired
        else:
            appointment_date = 'N/A'
            
        # Check if appointment_time is not None before formatting
            # appointment_time = instance.appointment_time.strftime('%H:%M')  # Format the time as desired
        if instance.appointment_time:
            appointment_time = instance.appointment_time.strftime('%H:%M')  # Format the time as desired
        else:
            appointment_time = 'N/A'
            
        message = (
            f'Dear {recipient_name},\n\n'
            f'We\'re pleased to inform you that your appointment with Dr. {doctor_name} has been approved.\n\n'
            f'Appointment Details:\n'
            f'- Doctor: Dr. {doctor_name}\n'
            f'- Date: {appointment_date}\n'
            f'- Time: {appointment_time}\n\n'
            f'Thank you for choosing our services. If you have any questions or need to reschedule, please don\'t hesitate to contact us.\n\n'
            f'Best regards,\n'
            f'Medilife.'
        )
        
        
        #TO SEND MAIL WITH THE COMPANY NAME HEADER AS THE SENDER
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False, headers={'From': 'Medilife Hospital <noreply@example.com>'})
        recipient_list = [recipient_email]
        approved_email = EmailMessage(
            subject=subject,
            body=message,
            from_email='Medilife Hospital <noreply@example.com>',
            to=recipient_list
        )
        approved_email.send()
        # send_mail(doc_subject, approved_doc_message, from_email, doc_recipient_list)
        doc_email = EmailMessage(
            subject=approved_doc_subjects,
            body=approved_doc_message,
            from_email='Medilife Hospital <noreply@example.com>',
            to=doc_recipient_list
        )
        doc_email.send()


