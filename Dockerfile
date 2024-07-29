FROM python:3.12.2-slim-bookworm

WORKDIR /var/www

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code
COPY app .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python3", "main.py"]