from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.registration_form, name='registration_form'),
    path('submit/', views.submit_registration, name='submit_registration'),
    path('confirmation/', views.confirmation, name='confirmation'),

    # Admin API (optional - for future use)
    path('admin-api/stats/',
         views.registration_stats, name='registration_stats'),
]
