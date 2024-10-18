from django import forms
from django.contrib.auth.models import User
from .models import Patient
# Doctor Signup Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Doctor

class DoctorSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    specialization = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'specialization', 'password1', 'password2']

    def save(self, commit=True):
        user = super(DoctorSignupForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # Using email as username
        if commit:
            user.save()
            # Save the Doctor profile (in case you have extra fields for doctor)
            doctor = Doctor(user=user, specialization=self.cleaned_data['specialization'])
            doctor.save()
        return user

# Add Patient Form
class AddPatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'dob', 'report']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date input
        }

# Report Upload Form (optional, if required separately)
class UploadReportForm(forms.Form):
    report = forms.FileField()
