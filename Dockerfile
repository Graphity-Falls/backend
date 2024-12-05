FROM python:3.10-slim

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Accept environment variables at build time (build arguments)
ARG GRAPHDB_URL
ARG CORS_ALLOWED_ORIGINS

# Set environment variables based on build arguments
ENV GRAPHDB_URL=${GRAPHDB_URL}
ENV CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS}

# Install pip requirements
COPY requirements.txt . 
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Create a non-root user with explicit UID
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden.
CMD ["gunicorn", "--workers", "3", "--log-level", "debug", "--bind", "0.0.0.0:8000", "graphity_falls.wsgi"]
