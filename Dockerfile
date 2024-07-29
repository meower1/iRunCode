FROM python:3.12.2-slim-bookworm

WORKDIR /var/www

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app .

CMD ["python3", "main.py"]