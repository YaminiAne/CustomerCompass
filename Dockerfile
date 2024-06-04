FROM python:3.7

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run gunicorn with 4 workers binding to 0.0.0.0:5000 and starting the Flask app
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:5000", "app:app"]
