FROM python:3.10-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/cities_app/
WORKDIR /usr/src/cities_app/

RUN apt-get update

COPY . /usr/src/cities_app/

RUN python -m pip install --no-cache-dir -r requirements/requirements.txt --use-deprecated=legacy-resolver

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]