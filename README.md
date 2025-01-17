README for Dockerized Application

This README provides a comprehensive guide to set up and run your application, which includes services for Django, PostgreSQL, Redis, Celery, and NGINX, all orchestrated using Docker Compose.

Table of Contents

Project Overview

Prerequisites

Folder Structure

Setup Instructions

Services

Environment Variables

Code Quality and Testing

How to Use

License

Project Overview

This project is a web application built with Django using the following technologies:

PostgreSQL: Database for storing structured data.

Django ORM & DRF: Backend framework and API tools.

Celery: For asynchronous task processing.

Redis: Message broker and caching layer.

JWT: For secure authentication.

GraphQL: Alternative to REST API for data querying.

NGINX: As a reverse proxy and static/media file server.

Logging: Integrated logging for easier debugging and monitoring.

Caching: Configured for optimal performance using Redis.

Testing: Unit and integration tests implemented to ensure code quality.

Code Quality Tools: Enforced standards using Black, Mypy, isort, and Flake8.

Prerequisites

Make sure you have the following installed:

Docker (20.10 or later)

Docker Compose (1.29 or later)

Python 3.9+ (for development purposes)

PostgreSQL client tools (optional)

Folder Structure

project/
├── testtask/          # Django application
├── nginx/             # NGINX configuration
│   └── nginx.conf
├── tests/             # Unit and integration tests
├── .env               # Environment variables
├── docker-compose.yml # Docker Compose configuration

Setup Instructions

1. Clone the Repository

git clone <repository_url>
cd project

2. Create and Configure the .env File

Create a .env file in the root directory with the following variables:

POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_postgres_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
SECRET_KEY=your_django_secret_key
DEBUG=True
REDIS_URL=redis://redis:6379/0

3. Build and Start Containers

Run the following commands:

docker-compose up --build -d

4. Verify the Setup

Access the application: http://localhost:8000

Static files: http://localhost/static/

Media files: http://localhost/media/

Services

1. PostgreSQL

Image: postgres:16.0

Volume: postgres_data for persisting database data.

Environment: Defined in .env.

2. Backend

Django application running with Gunicorn.

Performs migrations, collects static files, and serves the application.

3. Redis

Image: redis:7.2.3-alpine.

Used for Celery task queue and caching.

4. Celery

Processes asynchronous tasks and periodic jobs.

Uses Redis as a message broker.

5. NGINX

Serves as a reverse proxy for the Django application.

Serves static and media files.

Environment Variables

Variable

Description

POSTGRES_USER

PostgreSQL username

POSTGRES_PASSWORD

PostgreSQL password

POSTGRES_DB

PostgreSQL database name

POSTGRES_HOST

PostgreSQL host (default: db)

POSTGRES_PORT

PostgreSQL port (default: 5432)

SECRET_KEY

Django secret key

DEBUG

Django debug mode (True or False)

REDIS_URL

Redis URL for Celery and caching

Code Quality and Testing

1. Testing

Unit and integration tests are implemented to ensure the reliability of the application.
Run tests with:

docker-compose exec backend python3 manage.py test

2. Code Quality Tools

The following tools are used to maintain high code quality:

Black: Ensures consistent code formatting.

Mypy: Static type checking.

isort: Sorts imports in a consistent order.

Flake8: Lints the code for adherence to PEP 8 and other best practices.

Run All Code Quality Checks

black .
mypy .
isort .
flake8 .

3. Logging

The application includes robust logging configurations to debug and monitor.

4. Caching

Redis is configured as the caching layer for improved performance and response time.

How to Use

Run the Application

Start Containers:

docker-compose up -d

Check Logs:

docker-compose logs -f

Stop the Application

docker-compose down


