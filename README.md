# Django Backend for Bhudev Kalakaar 2025 Talent Event

This is a Django backend for the Bhudev Kalakaar 2025 talent event registration system.

## Features

- **Registration Management**: Complete registration system with photo uploads
- **API Endpoints**: RESTful API for frontend integration
- **Admin Panel**: Django admin interface for managing registrations
- **Statistics**: Real-time statistics and analytics
- **Activity Tracking**: Track all registration activities
- **File Upload**: Secure photo upload with validation
- **Email Notifications**: Automated confirmation emails
- **CORS Support**: Cross-origin resource sharing for frontend integration

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Registration API
- `POST /api/registrations/` - Create new registration
- `GET /api/registrations/` - List all registrations
- `GET /api/registrations/{id}/` - Get specific registration
- `GET /api/registrations/statistics/` - Get registration statistics

### Simple API
- `POST /api/submit/` - Submit registration (simpler endpoint)
- `GET /api/health/` - Health check

### Frontend URLs
- `/` - Registration form
- `/form/` - Alternative registration form URL
- `/confirmation/` - Confirmation page

## Admin Panel

Access the admin panel at `/admin/` with superuser credentials.

### Admin Features:
- View all registrations with filters and search
- Export registrations to CSV
- Manage registration status
- View registration activities
- Monitor daily statistics

## Models

### TalentEventRegistration
Main model storing participant information:
- Personal details (name, gender, DOB, age group)
- Event information (category, city)
- Contact details (WhatsApp number)
- Photo upload
- Terms agreement
- System tracking (IP, user agent, timestamps)

### RegistrationActivity
Tracks all activities related to registrations:
- Activity types (registration, photo upload, email sent, etc.)
- Descriptions and metadata
- Timestamps

### EventStatistics
Daily statistics:
- Total registrations
- Event-wise breakdown
- Age group distribution
- City-wise data

## Configuration

### Environment Variables
Create a `.env` file with:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Email Setup
Configure email settings in `settings.py` for sending confirmation emails.

### Media Files
Uploaded photos are stored in `/media/participant_photos/`

## Security Features

- CSRF protection
- File upload validation
- Image type validation
- File size limits (100MB)
- IP address tracking
- User agent logging

## Testing

Run tests with:
```bash
python manage.py test
```

## Production Deployment

1. Set `DEBUG=False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure email backend
5. Set up media file storage (AWS S3 recommended)
6. Use gunicorn for WSGI server

## API Usage Examples

### Submit Registration
```javascript
const formData = new FormData();
formData.append('full_name', 'John Doe');
formData.append('gender', 'male');
formData.append('date_of_birth', '15-08-1995');
formData.append('age_group', '21-40');
formData.append('event', 'singing');
formData.append('city', 'Mumbai');
formData.append('whatsapp_number', '9876543210');
formData.append('photo', photoFile);
formData.append('terms', 'yes');

fetch('/api/submit/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Get Statistics
```javascript
fetch('/api/registrations/statistics/')
.then(response => response.json())
.then(data => console.log(data));
```

## Support

For support and questions, contact the development team.
