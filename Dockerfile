FROM python:3.9.18-alpine3.19

RUN apk add --no-cache bash cmake make g++ curl git bash yasm pkgconfig gfortran openblas openblas-dev

# Install Chromaprint
RUN apk add --no-cache chromaprint-dev ffmpeg


WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]