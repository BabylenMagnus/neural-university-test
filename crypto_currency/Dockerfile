FROM python:latest

COPY . .

RUN pip install -r requirements.txt

ENV ALPHAVANTAGE_KEY="AIzaSyBKtWi7gMlWExJJ5hERBy69SrqBi0bRw9c"

EXPOSE 8020
EXPOSE 8110

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "runserver", "8020"]
