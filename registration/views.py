from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from django.utils import timezone
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging
import uuid

from .models import TalentEventRegistration, RegistrationActivity, EventStatistics

logger = logging.getLogger(__name__)


def registration_form(request):
    """Display the registration form"""
    return render(request, 'registration/form.html')


@csrf_exempt
@require_http_methods(["POST"])
def submit_registration(request):
    """Handle registration form submission"""
    try:
        # Extract and map form data from frontend to model fields
        frontend_data = {
            'fullName': request.POST.get('fullName'),
            'gender': request.POST.get('gender'),
            'dateOfBirth': request.POST.get('dateOfBirth'),
            'ageGroup': request.POST.get('ageGroup'),
            'event': request.POST.get('event'),
            'city': request.POST.get('city'),
            'whatsappNumber': request.POST.get('whatsappNumber'),
            'terms': request.POST.get('terms'),
        }

        # Handle photo upload
        photo = request.FILES.get('photo')

        # Create registration record with proper field mapping
        registration = TalentEventRegistration.objects.create(
            full_name=frontend_data['fullName'],
            gender=frontend_data['gender'],
            date_of_birth=frontend_data['dateOfBirth'],
            age_group=frontend_data['ageGroup'],
            event=frontend_data['event'],
            city=frontend_data['city'],
            whatsapp_number=frontend_data['whatsappNumber'],
            terms=frontend_data['terms'],
            photo=photo
        )

        # Log activity
        RegistrationActivity.objects.create(
            registration=registration,
            activity_type='registration',
            description=f"Registration created for {frontend_data['fullName']}"
        )        # Update statistics
        today = timezone.now().date()
        stats, created = EventStatistics.objects.get_or_create(
            date=today,
            defaults={
                'total_registrations': 0,
                'registrations_by_event': {},
                'registrations_by_age_group': {},
                'registrations_by_city': {}
            }
        )
        stats.total_registrations += 1

        # Update event-specific stats
        if frontend_data['event'] in stats.registrations_by_event:
            stats.registrations_by_event[frontend_data['event']] += 1
        else:
            stats.registrations_by_event[frontend_data['event']] = 1

        # Update age group stats
        if frontend_data['ageGroup'] in stats.registrations_by_age_group:
            stats.registrations_by_age_group[frontend_data['ageGroup']] += 1
        else:
            stats.registrations_by_age_group[frontend_data['ageGroup']] = 1

        # Update city stats
        if frontend_data['city'] in stats.registrations_by_city:
            stats.registrations_by_city[frontend_data['city']] += 1
        else:
            stats.registrations_by_city[frontend_data['city']] = 1

        stats.save()

        logger.info(f"Registration created successfully: ID {registration.id}")

        # Redirect to confirmation page
        return redirect('confirmation')

    except Exception as e:
        logger.error(f"Registration submission error: {str(e)}")
        messages.error(request, f"Registration failed: {str(e)}")
        return redirect('registration_form')


def confirmation(request):
    """Display confirmation page"""
    return render(request, 'registration/confirmation.html')

# Admin/API views for dashboard


def registration_stats(request):
    """Get registration statistics"""
    try:
        # Get today's stats or create if doesn't exist
        today = timezone.now().date()
        stats, created = EventStatistics.objects.get_or_create(
            date=today,
            defaults={
                'total_registrations': 0,
                'registrations_by_event': {},
                'registrations_by_age_group': {},
                'registrations_by_city': {}
            }
        )

        recent_registrations = TalentEventRegistration.objects.order_by(
            '-created_at')[:5]

        return JsonResponse({
            'success': True,
            'stats': {
                'total_registrations': stats.total_registrations,
                'registrations_by_event': stats.registrations_by_event,
                'registrations_by_age_group': stats.registrations_by_age_group,
                'registrations_by_city': stats.registrations_by_city,
                'date': stats.date.isoformat()
            },
            'recent_registrations': [
                {
                    'id': str(reg.id),
                    'full_name': reg.full_name,
                    'event': reg.event,
                    'age_group': reg.age_group,
                    'city': reg.city,
                    'created_at': reg.created_at.isoformat()
                } for reg in recent_registrations
            ]
        })
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
