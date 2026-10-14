FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Run python in unbuffered mode so logs appear instantly
CMD ["python", "-u", "main.py"]