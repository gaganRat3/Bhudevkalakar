from django.db import models
from django.utils import timezone
import uuid
import os


def participant_photo_path(instance, filename):
    """Generate file path for participant photos"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('participant_photos', filename)


class TalentEventRegistration(models.Model):
    """Model for storing talent event registration data"""

    # Choices for various fields
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    AGE_GROUP_CHOICES = [
        ('5-10', '5 Yrs to 10 Yrs'),
        ('11-20', '11 Yrs to 20 Yrs'),
        ('21-40', '21 Yrs to 40 Yrs'),
        ('41-above', '41 Yrs and Above'),
    ]

    EVENT_CHOICES = [
        ('singing', 'Singing'),
        ('dancing', 'Dancing'),
        ('musical-instrument', 'Musical Instrument'),
        ('others', 'Others'),
    ]

    TERMS_CHOICES = [
        ('yes', 'Yes, I Agree'),
        ('no', 'No, I Don\'t Agree'),
    ]

    # Primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Serial Number - Auto incrementing (for admin panel only)
    serial_number = models.PositiveIntegerField(
        unique=True, editable=False, null=True, blank=True, verbose_name="Serial Number")

    # Personal Information
    full_name = models.CharField(max_length=200, verbose_name="Full Name")
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, verbose_name="Gender")
    date_of_birth = models.CharField(
        max_length=10, verbose_name="Date of Birth (DD-MM-YYYY)")
    age_group = models.CharField(
        max_length=20, choices=AGE_GROUP_CHOICES, verbose_name="Age Group")

    # Event Information
    event = models.CharField(
        max_length=30, choices=EVENT_CHOICES, verbose_name="Event Category")
    city = models.CharField(
        max_length=100, verbose_name="Current Residence City")

    # Contact Information
    whatsapp_number = models.CharField(
        max_length=15, verbose_name="WhatsApp Number")

    # Photo Upload
    photo = models.ImageField(
        upload_to=participant_photo_path, verbose_name="Participant Photo")

    # Terms and Conditions
    terms = models.CharField(
        max_length=5, choices=TERMS_CHOICES, verbose_name="Terms & Conditions Agreement")

    # System Fields
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name="Registration Date")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Last Updated")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")

    # Additional tracking fields
    ip_address = models.GenericIPAddressField(
        null=True, blank=True, verbose_name="IP Address")
    user_agent = models.TextField(
        null=True, blank=True, verbose_name="User Agent")

    class Meta:
        verbose_name = "Talent Event Registration"
        verbose_name_plural = "Talent Event Registrations"
        ordering = ['serial_number']  # Order by serial number (1, 2, 3...)
        indexes = [
            models.Index(fields=['serial_number']),
            models.Index(fields=['created_at']),
            models.Index(fields=['event']),
            models.Index(fields=['age_group']),
            models.Index(fields=['city']),
        ]

    def __str__(self):
        return f"#{self.serial_number} - {self.full_name} - {self.get_event_display()}"

    @property
    def registration_id(self):
        """Generate a human-readable registration ID using serial number"""
        return f"BK2025-{str(self.serial_number).zfill(4)}"

    @property
    def photo_size_mb(self):
        """Get photo size in MB"""
        if self.photo:
            return round(self.photo.size / (1024 * 1024), 2)
        return 0

    def save(self, *args, **kwargs):
        """Custom save method with validation and auto serial number"""
        # Validate terms agreement
        if self.terms != 'yes':
            raise ValueError("Terms and conditions must be agreed to register")

        # Auto-generate serial number if not set
        if not self.serial_number:
            last_registration = TalentEventRegistration.objects.order_by(
                'serial_number').last()
            if last_registration:
                self.serial_number = last_registration.serial_number + 1
            else:
                self.serial_number = 1

        super().save(*args, **kwargs)


class RegistrationActivity(models.Model):
    """Model to track registration activities and logs"""

    ACTIVITY_CHOICES = [
        ('registration', 'Registration Submitted'),
        ('photo_uploaded', 'Photo Uploaded'),
        ('email_sent', 'Email Notification Sent'),
        ('video_submission', 'Video Submitted via WhatsApp'),
        ('status_update', 'Status Updated'),
    ]

    registration = models.ForeignKey(
        TalentEventRegistration,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    description = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Registration Activity"
        verbose_name_plural = "Registration Activities"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.registration.full_name} - {self.get_activity_type_display()}"


class EventStatistics(models.Model):
    """Model to store event statistics"""

    date = models.DateField(default=timezone.now)
    total_registrations = models.IntegerField(default=0)
    registrations_by_event = models.JSONField(default=dict)
    registrations_by_age_group = models.JSONField(default=dict)
    registrations_by_city = models.JSONField(default=dict)

    class Meta:
        verbose_name = "Event Statistics"
        verbose_name_plural = "Event Statistics"
        ordering = ['-date']
        unique_together = ['date']

    def __str__(self):
        return f"Statistics for {self.date}"
