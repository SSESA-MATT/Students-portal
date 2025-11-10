#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy configuration files if they exist
if [ -f "studetPortals/settings_new.py" ]; then
    cp studetPortals/settings_new.py studetPortals/settings.py
fi

if [ -f "studetPortals/urls_new.py" ]; then
    cp studetPortals/urls_new.py studetPortals/urls.py
fi

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate --no-input
