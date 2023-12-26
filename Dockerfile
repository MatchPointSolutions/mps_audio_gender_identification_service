FROM mpsacr.azurecr.io/myapp-base:spleeter

WORKDIR /app
COPY env_from_github_secrets .env
COPY . .
EXPOSE 7860
# CMD ["uvicorn", "test:app", "--host", "0.0.0.0", "--port", "7860"]

CMD ["sh", "-c", "gradio run main.py & tail -f /dev/null"]
