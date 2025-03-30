gunicorn core.wsgi:application --bind 0.0.0.0:10000 &
celery -A core worker --loglevel=info
