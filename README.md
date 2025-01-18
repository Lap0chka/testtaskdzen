# README for Dockerized Application

This README provides a comprehensive guide to set up and run your application, which includes services for Django, PostgreSQL, Redis, Celery, and NGINX, all orchestrated using Docker Compose.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Folder Structure](#folder-structure)
4. [Setup Instructions](#setup-instructions)
5. [Services](#services)
6. [Environment Variables](#environment-variables)
7. [Code Quality and Testing](#code-quality-and-testing)
8. [How to Use](#how-to-use)
9. [License](#license)

---

## Project Overview

This project is a web application built with Django using the following technologies:
- **PostgreSQL**: Database for storing structured data.
- **Django ORM & DRF**: Backend framework and API tools.
- **Celery**: For asynchronous task processing.
- **Redis**: Message broker and caching layer.
- **JWT**: For secure authentication.
- **GraphQL**: Alternative to REST API for data querying.
- **NGINX**: As a reverse proxy and static/media file server.
- **Logging**: Integrated logging for easier debugging and monitoring.
- **Caching**: Configured for optimal performance using Redis.
- **Testing**: Unit and integration tests implemented to ensure code quality.
- **Code Quality Tools**: Enforced standards using **Black**, **Mypy**, **isort**, and **Flake8**.

---

## Prerequisites

Make sure you have the following installed:
- **Docker** (20.10 or later)
- **Docker Compose** (1.29 or later)
- **Python 3.9+** (for development purposes)
- **PostgreSQL client tools** (optional)

---

## Folder Structure

```plaintext
project/
├── testtask/          # Django application
├── nginx/             # NGINX configuration
│   └── nginx.conf
├── tests/             # Unit and integration tests
├── .env               # Environment variables
├── docker-compose.yml # Docker Compose configuration
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd project
```

### 2. Create and Configure the `.env` File
Create a `.env` file in the root directory with the following variables:
```env
DEBUG=True/FAlse
SECRET_KEY=Django Key
POSTGRES_DB=your_postgres_db
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DB_HOST=host
DB_PORT=223
EMAIL_HOST_USER=google
EMAIL_HOST_PASSWORD=google
```

### 3. **Edit the `hosts` file**

- Locate and open the `hosts` file:
   - **Linux/macOS**: `/etc/hosts`
   - **Windows**: `C:\Windows\System32\drivers\etc\hosts`
   - Add the following line to the file:
     ```
     127.0.0.1    www.testtask.com testtask.com
     ```

**Save the changes**

- On Linux/macOS, you might need to use `sudo` to edit the file:
  ```bash
  sudo nano /etc/hosts
  ```
- On Windows, ensure that the text editor is run as an administrator.

### 4. Build and Start Containers
Run the following commands:
```bash
docker-compose up --build -d
```

### 5. Verify the Setup

- Access the application: [http://testtask.com](http://testtask.com)
- Static files: [http://testtask.com/static/](http://testtask.com/static/)
- Media files: [http://testtask.com/media/](http://testtask.com/media/)

---

## Services

### 1. **PostgreSQL**
- **Image**: `postgres:16.0`
- **Volume**: `postgres_data` for persisting database data.
- **Environment**: Defined in `.env`.

### 2. **Backend**
- **Django application** running with Gunicorn.
- Performs migrations, collects static files, and serves the application.

### 3. **Redis**
- **Image**: `redis:7.2.3-alpine`.
- Used for Celery task queue and caching.

### 4. **Celery**
- Processes asynchronous tasks and periodic jobs.
- Uses Redis as a message broker.

### 5. **NGINX**
- Serves as a reverse proxy for the Django application.
- Serves static and media files.

---

## Environment Variables

| Variable               | Description                          |
|------------------------|--------------------------------------|
| `POSTGRES_USER`        | PostgreSQL username                 |
| `POSTGRES_PASSWORD`    | PostgreSQL password                 |
| `POSTGRES_DB`          | PostgreSQL database name            |
| `POSTGRES_HOST`        | PostgreSQL host (default: `db`)     |
| `POSTGRES_PORT`        | PostgreSQL port (default: `5432`)   |
| `SECRET_KEY`           | Django secret key                   |
| `DEBUG`                | Django debug mode (`True` or `False`) |
| `REDIS_URL`            | Redis URL for Celery and caching    |

---

## Code Quality and Testing

### 1. **Testing**
Unit and integration tests are implemented to ensure the reliability of the application.
Run tests with:
```bash
docker-compose exec backend python3 manage.py test
```

### 2. **Code Quality Tools**
The following tools are used to maintain high code quality:
- **Black**: Ensures consistent code formatting.
- **Mypy**: Static type checking.
- **isort**: Sorts imports in a consistent order.
- **Flake8**: Lints the code for adherence to PEP 8 and other best practices.

#### Run All Code Quality Checks
```bash
black .
mypy .
isort .
flake8 .
```

### 3. **Logging**
The application includes robust logging configurations to debug and monitor.

### 4. **Caching**
Redis is configured as the caching layer for improved performance and response time.

---

## How to Use

### Run the Application
1. **Start Containers**:
   ```bash
   docker-compose up -d
   ```
2. **Check Logs**:
   ```bash
   docker-compose logs -f
   ```

### Stop the Application
```bash
docker-compose down
```

---


