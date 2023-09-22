FROM python:3.10.4-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
# CMD gunicorn --workers=2 --bind 0.0.0.0:$PORT app:app
CMD ["waitress-serve", "--listen=*:8080", "app:app"]