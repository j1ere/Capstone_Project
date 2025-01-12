release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn task_management_api.wsgi