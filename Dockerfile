FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8050
# CMD gunicorn --workers=2 --bind 0.0.0.0:$PORT app:app
CMD ["waitress-serve", "--listen=*:8050", "app:app"]