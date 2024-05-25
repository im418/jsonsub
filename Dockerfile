FROM python:3.11-alpine
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
CMD ["python", "main.py"]