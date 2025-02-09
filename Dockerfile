FROM python:3
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
COPY .env ./
CMD ["uvicorn", "app.main:app","--workers", "4" , "--host", "0.0.0.0", "--port", "8000"]