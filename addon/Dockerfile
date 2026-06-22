ARG BUILD_FROM=python:3.12-slim
FROM $BUILD_FROM
WORKDIR /app
COPY ../app/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ../app/backend/app ./app
COPY run.sh /run.sh
RUN chmod +x /run.sh
CMD ["/run.sh"]
