# sys_doc_scan/Dockerfile
FROM python:3.12.3-alpine3.19

ENV PYTHONUNBUFFERED 1

# Instalar dependencias necesarias
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    build-base \
    linux-headers \
    postgresql-dev

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "sysdocscan.wsgi:application"]
