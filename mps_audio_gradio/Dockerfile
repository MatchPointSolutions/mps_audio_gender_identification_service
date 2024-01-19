FROM python:3.9

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}
ENV FASTAPI_URL=http://api:8000

WORKDIR /workspace
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 7860
COPY . .
CMD ["python", "main.py"]