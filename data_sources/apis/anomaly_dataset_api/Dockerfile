# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy only requirements to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY data_api.py data_api.py

# Expose the port the app runs on
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "data_api:app", "--host", "0.0.0.0", "--port", "8000"]
