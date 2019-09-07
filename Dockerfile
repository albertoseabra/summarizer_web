FROM python:3.6-slim-stretch

RUN apt update
RUN apt install -y python3-dev gcc

COPY ./requirements.txt /web_app/requirements.txt

WORKDIR /web_app

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_md

COPY ./web_app /web_app

EXPOSE 5000

CMD [ "gunicorn", "-b", "0.0.0.0:5000", "web_flask:app" ]