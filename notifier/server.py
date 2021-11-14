import asyncio
import logging
from aiogram import Bot

from utils.queue import read_message
from utils import schema
from utils import config

bot = Bot(token=config.TELEGRAM_API_TOKEN)


@read_message(config.NOTIFICATION_QUEUE_NAME, schema.NLPMessageOutput)
async def handle_new_message(message_object: schema.NLPMessageOutput):
    """
    Notify client about a new message to telegram

    - save info about new message to db
    - send response message to telegram
    """

    logging.info('notifier: handle_new_message %s', message_object.message_id)
    await bot.send_message(message_object.chat_id, message_object.output_content)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handle_new_message())


if __name__ == '__main__':
    main()