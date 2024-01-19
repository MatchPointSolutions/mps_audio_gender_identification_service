FROM python:3.9

WORKDIR /app
# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    gcc \
    libchromaprint-tools \
    libchromaprint-dev \
    portaudio19-dev
RUN pip install spleeter


COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install protobuf==3.19.0