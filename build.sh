#!/usr/bin/env bash
# Build script for Render
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py compilemessages --ignore=.venv 2>/dev/null || echo "gettext not installed; using committed .mo files"
python manage.py migrate --noinput
python manage.py seed_content
