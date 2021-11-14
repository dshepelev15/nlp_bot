import asyncio
import aio_pika

import logging
import json
from dataclasses import asdict
from functools import wraps

from utils import config

async def write_message(queue_name, message_object):
    connection = await get_connection()
    channel = await connection.channel()

    body = json.dumps(asdict(message_object)).encode()
    logging.info("publish to queue %s message body: '%s'", queue_name, body)

    await channel.default_exchange.publish(
        aio_pika.Message(body=body),
        routing_key=queue_name
    )


def read_message(queue_name, message_schema_cls):
    logging.info("subscribe to queue %s", queue_name)

    def wrapper(func):
        @wraps(func)
        async def _wrapper(*args, **kwargs):
            connection = await get_connection()

            async with connection:
                channel = await connection.channel()
                queue = await channel.declare_queue(queue_name, durable=True)

                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process(ignore_processed=True):
                            try:
                                message_object = message_schema_cls(
                                    **json.loads(message.body.decode())
                                )
                                logging.info("process new message from queue %s message body: '%s'", queue_name, message_object)

                                await func(message_object)
                                await message.ack()

                            except Exception as exp:
                                logging.error('An error has occurred: %s', exp)
                                await message.reject(requeue=True)

        return _wrapper

    return wrapper


_connection = None

async def get_connection():
    global _connection
    if _connection is None:
        _connection = await aio_pika.connect_robust(config.RABBIT_HOSTNAME, loop=asyncio.get_event_loop())

    return _connection