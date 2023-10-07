FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY etl_script.py .

CMD ["python", "etl_script.py"]
  