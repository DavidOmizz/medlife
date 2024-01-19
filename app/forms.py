from django import forms
from .models import Doctor, Department,Appointment, Comment  # Import your Doctor and Department models
from phonenumber_field.formfields import PhoneNumberField

class AppointmentForm(forms.ModelForm):
    patient_name = forms.CharField(label='Full Name',widget=forms.TextInput(attrs={'placeholder': 'Enter full name', 'class': 'form-control', 'required': True})
    )
    patient_email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={'placeholder': 'Enter your email', 'type': 'email', 'class': 'form-control'})
    )
    # appointment_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'],widget=forms.TextInput(attrs={'placeholder': 'Enter your appointment date and time', 'type': 'datetime-local'})
    # )
    
    #Working on it...
    # appointment_date = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'Enter your appointment date', 'type': 'date','class': 'form-control'}))
    # appointment_time = forms.TimeField(widget=forms.TextInput(attrs={'placeholder': 'Enter your appointment time', 'type': 'time','class': 'form-control'}))
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),empty_label=None,widget=forms.Select(attrs={'required': True, 'class': 'form-control'}))
    
    # number = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'type': 'number'}), required=True)
    # number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),required=True)
    number = PhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control', 'id': 'phone_number'}),
        required=True,
        error_messages={'invalid': 'Enter a valid phone number (e.g., +12125552368)'}
    )
    department = forms.ModelChoiceField(queryset=Department.objects.all(),empty_label=None, widget=forms.Select(attrs={'required': True, 'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = ('patient_name', 'doctor', 'number', 'patient_email', 'department')

class ContactForm(forms.Form):
    name = forms.CharField(required=True, label = 'Name', widget= forms.TextInput(attrs={'placeholder':'Enter full name', 'class': 'form-control'}))
    email = forms.EmailField(required=True,label = 'email', widget= forms.TextInput(attrs={'placeholder':'Enter your mail', 'class': 'form-control'}))
    subject = forms.CharField(required=True,label = 'subject', widget= forms.TextInput(attrs={'placeholder':'Subject', 'class': 'form-control'}))
    message = forms.CharField(required=True,label = 'message', widget= forms.Textarea(attrs={'placeholder':'Message', 'class': 'form-control'}))
    # class Meta:
    #     model =Contact
    #     fields = ('name', 'email', 'subject', 'message')
    
class CommentForm(forms.ModelForm):
    name = forms.CharField(label = 'name', widget= forms.TextInput(attrs={'placeholder':'Enter full name', 'class': 'form-control'}))
    email = forms.EmailField(label = 'email', widget= forms.TextInput(attrs={'placeholder':'Enter your mail', 'class': 'form-control'}))
    body = forms.CharField(label = 'content', widget= forms.Textarea(attrs={'placeholder':'Message', 'class': 'form-control'}))
    class Meta:
        model =Comment
        fields = ('name', 'email', 'body')