"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types

from utils import config
from utils.queue import write_message
from utils.schema import NLPMessageInput
from utils.services.chat_message import save_chat_message
from utils.db.cassandra import create_session as create_cassandra_session


bot = Bot(token=config.TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)

"""

@dp.message_handler(commands=['select character'])
def get_all_available_characters():
    pass # get from postgres


def set_user_current_character():
    pass


"""


@dp.message_handler()
async def handle_text_message(message: types.Message):
    chat_message = await save_chat_message(
        content=message.text,
        chat_id=message.chat.id,
        from_user_id=message.from_user.id,
        character_id=1, # TODO retrieve from postgres
    )

    message_object = NLPMessageInput(
        message_id=str(chat_message.id),
        input_content=message.text,
        character_id=1,
        chat_id=message.chat.id,
    )

    await write_message(queue_name=config.NLP_COMMON_PREPROCESSING_QUEUE_NAME, message_object=message_object)


if __name__ == '__main__':
    # Setup connection for cqlengine
    session = create_cassandra_session()
    executor.start_polling(dp, skip_updates=True)
