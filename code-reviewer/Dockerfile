FROM python:3.12-slim

WORKDIR /reviewer-app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:8001 & celery -A core worker --loglevel=info"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
