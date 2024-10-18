from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.doctor_auth, name='doctor_auth'),  # Combined login/signup page
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('search-doctors/', views.search_doctors, name='search_doctors'),
]


