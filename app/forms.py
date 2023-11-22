from django import forms
from .models import Doctor, Department,Appointment  # Import your Doctor and Department models

class AppointmentForm(forms.ModelForm):
    patient_name = forms.CharField(label='Full Name',widget=forms.TextInput(attrs={'placeholder': 'Enter full name', 'required': True})
    )
    patient_email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={'placeholder': 'Enter your email', 'type': 'email'})
    )
    # appointment_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'],widget=forms.TextInput(attrs={'placeholder': 'Enter your appointment date and time', 'type': 'datetime-local'})
    # )
    appointment_date = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'Enter your appointment date', 'type': 'date'})
    )
    appointment_time = forms.TimeField(widget=forms.TextInput(attrs={'placeholder': 'Enter your appointment time', 'type': 'time'})
    )
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),empty_label=None,widget=forms.Select(attrs={'required': True}))
    number = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'type': 'number'}), required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(),empty_label=None, widget=forms.Select(attrs={'required': True})
    )

    class Meta:
        model = Appointment
        fields = ('patient_name', 'appointment_date', 'appointment_time', 'doctor', 'number', 'patient_email', 'department')
