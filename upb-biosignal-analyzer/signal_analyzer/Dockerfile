# Base Python image
FROM python:3.10.15

# Set working directory
WORKDIR /app

# Copy only what’s needed
COPY ./app ./app
COPY ./requirements.txt .

# Ensure Python sees the app folder
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
