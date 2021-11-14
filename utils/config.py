import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO
)


TELEGRAM_API_TOKEN = os.environ['TELEGRAM_API_TOKEN']
HUGGING_FACE_API_TOKEN = os.environ['HUGGING_FACE_API_TOKEN']

CASSANDRA_USER = os.environ['CASSANDRA_USER']
CASSANDRA_PASSWORD = os.environ['CASSANDRA_PASSWORD']


RABBIT_HOSTNAME="amqp://test:test@rabbitmq/"

# REDIS_HOSTNAME = 'localhost' # redis
IS_TEST = 'pytest' in sys.argv[0] # "PYTEST_CURRENT_TEST" in os.environ
REDIS_HOSTNAME = '0.0.0.0' if IS_TEST else 'redis'
CASSANDRA_NODES = ['0.0.0.0'] if IS_TEST else ['cassandra']

RABBIT_HOST = '0.0.0.0' if IS_TEST else 'rabbitmq'
RABBIT_HOSTNAME = f"amqp://test:test@{RABBIT_HOST}/"



NLP_COMMON_PREPROCESSING_QUEUE_NAME = 'nlp_common_preprocess'
NLP_INFERENCE_QUEUE_NAME_TEMPLATE = 'nlp_inference_character_{}'

NOTIFICATION_QUEUE_NAME = 'notifier'