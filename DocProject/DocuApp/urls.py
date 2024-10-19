from django.urls import path
from . import views
from DocuApp import views as DocuApp_views
from .views import forgot_password


urlpatterns = [
    path('', DocuApp_views.home, name='home'),
    path('auth/', views.doctor_auth, name='doctor_auth'),  # Combined login/signup page
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('search-doctors/', views.search_doctors, name='search_doctors'),
    path('doctor-portal/', DocuApp_views.doctor_auth, name='doctor_auth'),
    path('patient-portal/', DocuApp_views.patient_login, name='patient_login'),
    path('help/', DocuApp_views.help_page, name='help_page'),
    path('appointments/', DocuApp_views.appointments_page, name='appointments_page'),
    path('articles/', DocuApp_views.articles_page, name='articles_page'),
    path('feedback/', DocuApp_views.feedback_page, name='feedback_page'),
    path('contact/', DocuApp_views.contact_page, name='contact_page'),
    path('search-doctors/', DocuApp_views.search_doctors, name='search_doctors'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
    path('forgot-password/', DocuApp_views.forgot_password, name='forgot_password'),

]



