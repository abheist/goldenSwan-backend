release: python manage.py migrate
heroku config:set DISABLE_COLLECTSTATIC=1
web: gunicorn meup.wsgi