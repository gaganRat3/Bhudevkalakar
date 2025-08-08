from rest_framework import serializers
from .models import TalentEventRegistration, RegistrationActivity


class TalentEventRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for TalentEventRegistration model"""

    registration_id = serializers.ReadOnlyField()
    photo_size_mb = serializers.ReadOnlyField()

    class Meta:
        model = TalentEventRegistration
        fields = [
            'id', 'registration_id', 'full_name', 'gender', 'date_of_birth',
            'age_group', 'event', 'city', 'whatsapp_number', 'photo',
            'photo_size_mb', 'terms', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_terms(self, value):
        """Validate that terms are agreed to"""
        if value != 'yes':
            raise serializers.ValidationError(
                "You must agree to the terms and conditions to register.")
        return value

    def validate_photo(self, value):
        """Validate photo file"""
        if value:
            # Check file size (max 100MB)
            if value.size > 100 * 1024 * 1024:
                raise serializers.ValidationError(
                    "Photo size should not exceed 100MB.")

            # Check file type
            allowed_types = ['image/jpeg',
                             'image/png', 'image/jpg', 'image/gif']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Only JPEG, PNG, and GIF images are allowed.")

        return value

    def validate_date_of_birth(self, value):
        """Validate date of birth format"""
        import re
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', value):
            raise serializers.ValidationError(
                "Date of birth must be in DD-MM-YYYY format.")
        return value

    def validate_whatsapp_number(self, value):
        """Validate WhatsApp number"""
        import re
        # Remove any non-digit characters
        cleaned_number = re.sub(r'\D', '', value)

        # Check if it's a valid length (10-15 digits)
        if len(cleaned_number) < 10 or len(cleaned_number) > 15:
            raise serializers.ValidationError(
                "Please enter a valid WhatsApp number.")

        return value


class RegistrationActivitySerializer(serializers.ModelSerializer):
    """Serializer for RegistrationActivity model"""

    class Meta:
        model = RegistrationActivity
        fields = ['id', 'activity_type',
                  'description', 'timestamp', 'metadata']
        read_only_fields = ['id', 'timestamp']


class RegistrationSummarySerializer(serializers.ModelSerializer):
    """Simplified serializer for registration summaries"""

    registration_id = serializers.ReadOnlyField()
    event_display = serializers.CharField(
        source='get_event_display', read_only=True)
    age_group_display = serializers.CharField(
        source='get_age_group_display', read_only=True)
    gender_display = serializers.CharField(
        source='get_gender_display', read_only=True)

    class Meta:
        model = TalentEventRegistration
        fields = [
            'id', 'registration_id', 'full_name', 'gender_display',
            'age_group_display', 'event_display', 'city', 'created_at'
        ]
