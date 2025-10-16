FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install sharepy

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY crontab.txt /etc/cron.d/approvals-cron

# Creamos dir de cache para device code 
RUN mkdir -p /.token_cache && chmod -R 777 /.token_cache
#CMD ["python","-u","src/main.py"]

RUN chmod 0644 /etc/cron.d/approvals-cron
#RUN crontab /etc/cron.d/approvals-cron
RUN touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log