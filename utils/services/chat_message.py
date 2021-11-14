from utils.models import ChatMessage
from utils.schema import ContentType, NLPMessageOutput

BOT_USER_ID = -1


async def save_replied_message(nlp_output: NLPMessageOutput) -> ChatMessage:
    message = await get_chat_message_by_id(nlp_output.message_id)
    replied_message = await save_chat_message(
        content=nlp_output.output_content,
        chat_id=message.chat_id,
        to_user_id=message.to_user_id,
        from_user_id=BOT_USER_ID,
        reply_chat_message_id=nlp_output.message_id,
        character_id=message.character_id,
    )
    return replied_message


async def save_chat_message(**kwargs):
    if 'to_user_id' not in kwargs:
        kwargs['to_user_id'] = BOT_USER_ID

    if 'content_type' not in kwargs:
        kwargs['content_type'] = ContentType.TEXT

    return await ChatMessage.objects.async_create(**kwargs)


async def get_chat_message_by_id(message_id) -> ChatMessage:
    return await ChatMessage.objects.async_get(id=message_id)

