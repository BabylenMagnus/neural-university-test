FROM ubuntu

COPY github_api.py ./app.py
COPY cred.json ./cred.json

RUN apt-get update && apt-get -y install python3-pip

RUN pip3 install google-api-python-client oauth2client httplib2 Flask requests

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
