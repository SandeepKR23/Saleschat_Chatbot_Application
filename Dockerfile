FROM python:3.8-slim-buster
WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y

RUN apt-get update && pip install -r requirements.txt
RUN mkdir /opt/ect

# Specify the command to start your ASGI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
