FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd --uid 10001 --create-home appuser

USER 10001:10001

EXPOSE 5000

CMD ["python", "app.py"]