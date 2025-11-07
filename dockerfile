FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY run.sh .
COPY crontab.txt /etc/cron.d/approvals-cron

RUN chmod 0644 /etc/cron.d/approvals-cron
RUN crontab /etc/cron.d/approvals-cron

CMD ["bash", "run.sh"]
