FROM python:3.12.2-slim-bookworm

WORKDIR /var/www

COPY requirements.txt .

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY app .

CMD ["python3", "main.py"]