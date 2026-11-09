release: python manage.py migrate --noinput && python manage.py seed_content
web: gunicorn config.wsgi --log-file -
