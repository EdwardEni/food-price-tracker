# Use official Python image with slim base
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first (if you have requirements.txt)
COPY ../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy API source code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
