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


@login_required
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
