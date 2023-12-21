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
EXPOSE 7860

# CMD ["uvicorn", "test:app", "--host", "0.0.0.0", "--port", "7860"]

CMD ["python", "main.py"]