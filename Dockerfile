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

COPY requirements.txt .
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]