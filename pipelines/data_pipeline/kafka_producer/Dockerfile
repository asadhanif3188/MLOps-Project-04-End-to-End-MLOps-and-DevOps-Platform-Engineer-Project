# Use an official Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY main.py .

# Set the command to run the producer script
CMD ["python", "main.py"]
