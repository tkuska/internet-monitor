FROM python:3.11-slim


ENV TZ=Europe/Warsaw
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    curl \
    cron \
    iproute2 \
    gnupg \
 && curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | bash \
 && apt-get install -y speedtest \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app

RUN echo "*/30 * * * * /usr/local/bin/python3 /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/speedtest
RUN chmod 0644 /etc/cron.d/speedtest
RUN crontab /etc/cron.d/speedtest

VOLUME ["/data"]

CMD python /app/main.py \
 && cron \
 && gunicorn --bind 0.0.0.0:5000 --workers 3 web:app
