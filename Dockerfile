FROM python:3.7

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app

RUN pip install -r requirements.txt

ADD . /app

# setup database migrations here
RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD exec gunicorn healthid.wsgi --bind 0.0.0.0:8000