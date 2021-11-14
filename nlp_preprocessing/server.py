import asyncio
from dataclasses import asdict

import pymorphy2


from utils.queue import read_message, write_message
from utils import schema
from utils import config


@read_message(config.NLP_COMMON_PREPROCESSING_QUEUE_NAME, schema.NLPMessageInput)
async def handle_new_message(message_object: schema.NLPMessageInput):
    # message_object.input_content = lemmatize(message_object.input_content) # just for usage example

    nlp_inference_queue_name = config.NLP_INFERENCE_QUEUE_NAME_TEMPLATE.format(message_object.character_id)
    await write_message(
        queue_name=nlp_inference_queue_name,
        message_object=schema.NLPMessageInput(**asdict(message_object))
    )


def lemmatize(text):
    words = text.split()
    result = []
    for word in words:
        word = word.strip()
        if not word:
            continue

        p = morph.parse(word)[0]
        result.append(p.normal_form)

    return ' '.join(result)


if __name__ == '__main__':
    morph = pymorphy2.MorphAnalyzer()

    loop = asyncio.get_event_loop()
    loop.create_task(handle_new_message(None))
    loop.run_forever()
