# Caras/MachineFlow

The task (in Ukrainian):
https://docs.google.com/document/d/1XosiR4hKvPGQygrghGGTZAT_ntAiVPNxkJOz8i71kB0

## Getting started

This guide will take you through the steps to set up and run the project on your device.

### Installation

Steps to install the project in a standart way:

1. Clone the repository: https://github.com/FTKV/python-data-science-course-project

2. Go to the project directory: `cd python-data-science-course-project`

3. Create, fill with settings file `.env` with following format:

```
API_NAME=Caras-MachineFlow
API_PROTOCOL=http
API_HOST=0.0.0.0
API_PORT=8000

SECRET_KEY_LENGTH=64
ALGORITHM=HS512

DATABASE=postgresql
DRIVER_SYNC=psycopg2
DRIVER_ASYNC=asyncpg
POSTGRES_DB=...
POSTGRES_USER=${POSTGRES_DB}
POSTGRES_PASSWORD=...
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
SQLALCHEMY_DATABASE_URL_SYNC=${DATABASE}+${DRIVER_SYNC}://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
SQLALCHEMY_DATABASE_URL_ASYNC=${DATABASE}+${DRIVER_ASYNC}://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

REDIS_PROTOCOL=redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_USER=...
REDIS_PASSWORD=...
REDIS_URL=${REDIS_PROTOCOL}://${REDIS_USER}:${REDIS_PASSWORD}@${REDIS_HOST}:${REDIS_PORT}
REDIS_EXPIRE=3600
REDIS_DB_FOR_RATE_LIMITER=0
REDIS_DB_FOR_OBJECTS=1
REDIS_DB_FOR_APSCHEDULER=2

RATE_LIMITER_TIMES=2
RATE_LIMITER_SECONDS=5

MAIL_SERVER=...
MAIL_PORT=465
MAIL_USERNAME=...
MAIL_PASSWORD=...
MAIL_FROM=test@test.com
MAIL_FROM_NAME=${API_NAME}

CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

TENSORFLOW_CONTAINER_NAME=tensorflow-model
TENSORFLOW_MODEL_PATH=./models
TENSORFLOW_DOCKERFILE_NAME=dockerfile_model
TENSORFLOW_PORT=8001

TEST=False
```

4. Run Postgres DB, Redis DB, CV app and main app with Docker by `docker-compose up -d`

5. Open http://127.0.0.1:8000 or http://127.0.0.1:8000/docs to open the project's Swagger documentation (The API protocol, host and port you can change with .env)

### The authors

Identity team
