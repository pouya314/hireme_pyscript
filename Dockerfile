FROM python:3.11.4

RUN apt-get update
RUN apt-get install -y curl  # Install curl package for Kamal

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:3000"]
