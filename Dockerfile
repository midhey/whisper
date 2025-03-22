FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY transcribe.py transcribe.py
COPY logger.py logger.py

CMD ["python", "transcribe.py"]

