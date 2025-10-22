# Stage 1: Builder
FROM python:3.12-slim as builder

# Set Poetry environment variables for virtualenv creation within the project
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get install pipx -y

# Install Poetry
RUN pipx install poetry

WORKDIR /app

# Copy project files necessary for dependency installation
COPY src/pyproject.toml src/poetry.lock ./

# Install project dependencies
RUN poetry install --no-root --only main

# Stage 2: Runtime
FROM python:3.12-slim as runtime

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the application code
COPY src/python-app .

# Add the virtual environment's bin directory to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Define the command to run your application
CMD ["python", "__init__.py"]