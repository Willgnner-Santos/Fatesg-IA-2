FROM python:3.12-slim
WORKDIR /memcached
COPY . /memcached
COPY . /memcached
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "memcached.py"]