FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start the Dash app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dash_app:server"]
