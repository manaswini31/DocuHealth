from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
# Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


def validate_dob(value):
    if value > timezone.now().date():
        raise ValidationError("Date of birth cannot be in the future.")

class Patient(models.Model):
    doctor = models.ForeignKey(
        'Doctor', 
        on_delete=models.CASCADE, 
        related_name='patients'  # Allows access to patients via doctor.patients.all()
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(validators=[validate_dob])  # Ensure the date of birth is not in the future
    report = models.FileField(upload_to='reports/')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.patient_id} (Doctor: {self.doctor})'

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP is valid for 10 minutes
        return (timezone.now() - self.created_at).total_seconds() <= 600

    def __str__(self):
        return f"{self.user.email} - {self.otp_code}"
