# syntax=docker/dockerfile:1

# Base image
FROM python:3.10

# Optimize Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /messaging_app

# Create non-root user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=Requirements.txt,target=Requirements.txt \
    python -m pip install -r Requirements.txt

# Switch to app user
USER appuser

# Copy project files
COPY . .

# Expose app port
EXPOSE 8000

# Start application
CMD [ "python3", "./entry_point.py" ]
