FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make the script executable
COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh

# Use the start script as the entrypoint
ENTRYPOINT ["/start.sh"]

# The command from docker-compose will be passed to the entrypoint script
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 