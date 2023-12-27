FROM python:3.9

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

WORKDIR /workspace
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 7860
COPY . .
CMD ["python", "main.py"]