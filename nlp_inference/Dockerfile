FROM python:3.9

WORKDIR /code

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY utils utils
COPY nlp_inference nlp_inference

ENTRYPOINT ["python3.9", "-O", "-m", "nlp_inference.server_character_1"]
CMD [""]