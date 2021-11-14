import asyncio
import logging
from dataclasses import asdict

from utils.queue import read_message, write_message
from utils.huggingface_models.blender import inference_blender
from utils.text_preparation import (
    get_prepared_huggingface_payload,
    save_huggingface_response_and_get_generated_replica,
)
from utils.db.cassandra import create_session as create_cassandra_session
from utils.services.chat_message import save_replied_message
from utils import schema
from utils import config


CHARACTER_ID = '1' # TODO add to argparse / character and model path (or huggingface api url)

NLP_INFERENCE_QUEUE_NAME = config.NLP_INFERENCE_QUEUE_NAME_TEMPLATE.format(CHARACTER_ID)


@read_message(NLP_INFERENCE_QUEUE_NAME, schema.NLPMessageInput)
async def handle_new_message(message_object: schema.NLPMessageInput):
    huggingface_payload = await get_prepared_huggingface_payload(message_object.chat_id, message_object.input_content)
    response = await inference_blender(huggingface_payload)
    generated_replica = await save_huggingface_response_and_get_generated_replica(
        message_object.chat_id, message_object.input_content, response
    )

    output_object = dict(**asdict(message_object), output_content=generated_replica)
    output_message_object = schema.NLPMessageOutput(**output_object)

    await save_replied_message(output_message_object)
    await write_message(
        queue_name=config.NOTIFICATION_QUEUE_NAME,
        message_object=output_message_object
    )


if __name__ == '__main__':
    # Setup connection for cqlengine
    session = create_cassandra_session()
    asyncio.get_event_loop().run_until_complete(handle_new_message(None))