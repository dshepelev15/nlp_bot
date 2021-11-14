FROM python:3.9

WORKDIR /code

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY utils utils
COPY nlp_preprocessing nlp_preprocessing

ENTRYPOINT ["python3.9", "-O", "-m", "nlp_preprocessing.server"]
CMD [""]