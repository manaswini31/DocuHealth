from django.shortcuts import render
from django.db.models import Q  # Correct import for Q
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from .models import Patient
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Doctor, Patient
from .forms import DoctorSignupForm, AddPatientForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

import random
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
# Doctor Sign Up and Login (combined in one page)

def doctor_auth(request):
    signup_form = DoctorSignupForm()
    login_error = None
    
    # Handle Sign Up
    if request.method == 'POST' and 'signup' in request.POST:
        signup_form = DoctorSignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.set_password(signup_form.cleaned_data['password1'])
            user.save()
            doctor = Doctor(user=user, specialization=request.POST['specialization'])
            doctor.save()
            return redirect('doctor_dashboard')

    # Handle Login
    if request.method == 'POST' and 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'doctor'):
            login(request, user)
            return redirect('doctor_dashboard')
        else:
            login_error = 'Invalid username or password'

    return render(request, 'registration/login.html', {
        'signup_form': signup_form,
        'login_error': login_error,
    })

# Doctor Dashboard
@login_required
def doctor_dashboard(request):
    doctor = request.user.doctor
    patients = Patient.objects.filter(doctor=doctor)
    return render(request, 'DocuApp/doctor_dashboard.html', {'doctor': doctor, 'patients': patients})

def patient_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('patient_dashboard')  # Redirect to patient dashboard
            else:
                return render(request, 'registration/patient_login.html', {'form': form, 'error': 'Invalid credentials'})
    
    form = AuthenticationForm()
    return render(request, 'registration/patient_login.html', {'form': form})


def patient_dashboard(request):
    # Fetch the patient associated with the logged-in user
    patient = get_object_or_404(Patient, user=request.user)
    return render(request, 'DocuApp/patient_dashboard.html', {'patient': patient})

@login_required
def add_patient(request):
    if request.method == 'POST':
        form = AddPatientForm(request.POST, request.FILES)
        if form.is_valid():
            # Generate a unique patient ID (e.g., based on timestamp or custom logic)
            patient_id = generate_patient_id()  # Generate a unique patient ID

            # Create Patient's User credentials with the same username as patient_id
            patient_user = User.objects.create_user(
                username=patient_id, 
                password=form.cleaned_data['dob'].strftime('%Y-%m-%d')
            )
            patient_user.save()

            # Create Patient instance and link to the newly created User
            patient = form.save(commit=False)
            patient.user = patient_user  # Link the created user
            patient.doctor = request.user.doctor
            patient.patient_id = patient_id  # Set the patient ID
            patient.save()

            return redirect('doctor_dashboard')
    else:
        form = AddPatientForm()
    
    return render(request, 'DocuApp/add_patient.html', {'form': form})


# DocuApp/views.py

from django.shortcuts import render
from django.db.models import Q
from .models import Doctor

def search_doctors(request):
    query = request.GET.get('q')
    doctors = Doctor.objects.all()
    
    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(specialization__icontains=query)
        )
    
    return render(request, 'DocuApp/search_doctors.html', {'doctors': doctors, 'query': query})


# Generate a unique patient ID (e.g., based on timestamp or custom logic)
import time
def generate_patient_id():
    return str(int(time.time()))  # Example: timestamp-based unique ID
# views.py


def home(request):
    return render(request, 'DocuApp/home.html')

def appointments_page(request):
    return render(request, 'DocuApp/appointments.html')

def articles_page(request):
    return render(request, 'DocuApp/articles.html')

def feedback_page(request):
    return render(request, 'DocuApp/feedback.html')

def contact_page(request):
    return render(request, 'DocuApp/contact.html')

def help_page(request):
    return render(request, 'DocuApp/help.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.forms import SetPasswordForm
from .models import OTPVerification
import random

# DocuApp/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import OTPVerification
import random

# views.py

from django.contrib.auth.models import User

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            # Use filter() to get the first user with this email
            user = User.objects.filter(email=email).first()
            if not user:
                return render(request, 'DocuApp/send_otp.html', {'error': 'User with this email does not exist.'})

            otp_code = str(random.randint(100000, 999999))

            # Save or update the OTP for the user
            otp_verification, created = OTPVerification.objects.get_or_create(user=user)
            otp_verification.otp_code = otp_code
            otp_verification.save()

            # Send email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp_code}. It is valid for 10 minutes.',
                'from@example.com',  # Replace with your email address
                [email],
                fail_silently=False,
            )
            return redirect('verify_otp', user_id=user.id)
        except Exception as e:
            return render(request, 'DocuApp/send_otp.html', {'error': str(e)})

    return render(request, 'DocuApp/send_otp.html')




def verify_otp(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        otp_verification = OTPVerification.objects.filter(user=user, otp_code=otp_code).first()

        if otp_verification and otp_verification.is_valid():
            return redirect('reset_password', user_id=user.id)
        else:
            return render(request, 'DocuApp/verify_otp.html', {'user': user, 'error': 'Invalid or expired OTP.'})

    return render(request, 'DocuApp/verify_otp.html', {'user': user})


def reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SetPasswordForm(user)

    return render(request, 'DocuApp/reset_password.html', {'form': form})
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User


def forgot_password(request):
    if request.method == 'POST':
        # Handle sending the OTP
        if 'send_otp' in request.POST:
            email = request.POST.get('email')

            # Check if the email exists in the auth_user table
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Email not found in our system.")
                return redirect('forgot_password')  # Redirect to the same page

            # Generate a 6-digit OTP
            otp = random.randint(100000, 999999)

            # Send OTP email via Mailgun
            send_mail(
                subject='Password Reset OTP',
                message=f'Your OTP for password reset is {otp}.',
                recipient_list=[email],
                fail_silently=False,
                from_email='2100069015@kluniversity.in',  # Ensure this email is verified in Mailgun
            )

            # Save OTP and user ID to session
            request.session['otp'] = otp
            request.session['user_id'] = user.id
            request.session['email'] = email  # Store email for later use

            messages.success(request, "OTP sent to your email address.")
            # No redirect here to keep the email form visible

        # Handle verifying the OTP
        elif 'verify_otp' in request.POST:
            otp_input = request.POST.get('otp')
            if str(request.session.get('otp')) == otp_input:
                # OTP is valid, proceed to reset password
                messages.success(request, "OTP verified successfully! You can now reset your password.")
                return redirect('reset_password', user_id=request.session['user_id'])  # Redirect with user_id
            else:
                messages.error(request, "Invalid OTP. Please try again.")

    # Render the template with any messages
    return render(request, 'DocuApp/forgot_password.html')