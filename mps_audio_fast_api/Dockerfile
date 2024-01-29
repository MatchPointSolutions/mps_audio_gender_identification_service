FROM mpsacr.azurecr.io/myapp-base:spleeter
WORKDIR /app
COPY  /. .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
