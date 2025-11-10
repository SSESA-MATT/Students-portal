# Procfile for Heroku/Railway deployment

# Web process: Run gunicorn server
web: gunicorn studetPortals.wsgi:application --bind 0.0.0.0:$PORT --workers 3

# Release command: Run migrations before deployment
release: python manage.py migrate --noinput
