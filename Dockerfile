FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl gcc libpq-dev build-essential nodejs npm \
    && rm -rf /var/lib/apt/lists/*

# Install TailwindCSS globally (optional)
RUN npm install -g tailwindcss

# Install Poetry
ENV POETRY_VERSION=1.8.5
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

# Set Poetry environment variables
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="/root/.local/bin:$PATH"

# Copy only necessary files for Poetry dependency installation
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

#This is only for render setup!
# Install TailwindCSS globally
RUN npm install -g tailwindcss


# Copy the rest of the application files
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONWARNINGS="ignore::DeprecationWarning"

# Expose Flask port
EXPOSE 5000

# Run the Flask application
#CMD ["sh", "-c", "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch & flask run --host=0.0.0.0 --reload"]
CMD ["sh", "-c", "npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch & flask run --host=0.0.0.0 --port=5000"]




