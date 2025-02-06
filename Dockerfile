FROM python:3.12

# Set working directory
WORKDIR /app

# Install Poetry
ENV POETRY_VERSION=1.8.5
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

# Copy only necessary files for Poetry
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONWARNINGS="ignore::DeprecationWarning"

# Expose Flask port
EXPOSE 5000

# Run Flask server
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]