from uuid import uuid4
from datetime import datetime

from aiocqlengine.models import AioModel
from cassandra.cqlengine import columns


class ChatMessage(AioModel):
    """
    Model for storing messages in Cassandra DB
    """
    id = columns.UUID(primary_key=True, default=uuid4)
    created_at = columns.DateTime(default=datetime.now)
    content = columns.Text()
    content_type = columns.Text()
    from_user_id = columns.Integer(custom_index=True, required=True)
    to_user_id = columns.Integer(custom_index=True, required=True)
    chat_id = columns.Integer(custom_index=True, required=True)

    character_id = columns.Integer()
    reply_chat_message_id = columns.UUID()
