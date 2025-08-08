# Simple production settings for deployment
import os
from .settings import *

# Override development settings for production
DEBUG = False

# Use environment variable for secret key in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Static files for production (simple version)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Keep database as SQLite for simplicity
# (SQLite works fine for small to medium applications)
