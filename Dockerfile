# Pull official base Python Docker image
FROM python:3.10.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libc-dev \
    && pip install uwsgi \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy the Django project
COPY . /code/

