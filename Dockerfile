
FROM python:3.9-slim


WORKDIR /app

COPY requirements.txt /app/

# Update the package index and install GCC
RUN apt-get update \
    && apt-get install -y gcc \
                          libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt


COPY . /app/


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]