FROM python:3.11-slim
WORKDIR /app
COPY iot_sim.py /app/
RUN pip install flask prometheus_client
EXPOSE 8085
CMD ["python", "iot_sim.py"]

