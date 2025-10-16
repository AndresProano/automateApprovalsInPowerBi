FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /app/src/
# Creamos dir de cache para device code (si lo usas)
RUN mkdir -p /.token_cache && chmod -R 777 /.token_cache
CMD ["python","-u","src/main.py"]