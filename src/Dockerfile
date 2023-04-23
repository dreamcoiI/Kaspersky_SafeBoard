FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt pip install uvicorn jinja2

COPY word_count.py .
COPY static/result.txt .
COPY text.txt .

COPY . .

CMD [ "python3", "main.py" ]
