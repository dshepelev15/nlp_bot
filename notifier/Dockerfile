FROM python:3.9

WORKDIR /code

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY utils utils
COPY notifier notifier

ENTRYPOINT ["python3.9", "-O", "-m", "notifier.server"]
CMD [""]