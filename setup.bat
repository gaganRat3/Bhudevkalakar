@echo off
echo Starting Bhudev Kalakaar 2025 Django Backend...
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Applying database migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Creating static files directory...
python manage.py collectstatic --noinput

echo.
echo Django backend setup complete!
echo.
echo To start the development server, run:
echo python manage.py runserver
echo.
echo To create an admin user, run:
echo python manage.py createsuperuser
echo.
pause
