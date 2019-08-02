FROM python:3.6

COPY ./requirements.txt /web_app/requirements.txt

WORKDIR /web_app

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_md

COPY ./web_app /web_app

EXPOSE 5000

CMD [ "python", "web_flask.py" ]