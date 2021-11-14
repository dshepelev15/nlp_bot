from uuid import uuid4
from datetime import datetime

from aiocqlengine.models import AioModel
from cassandra.cqlengine import columns


class CharacterUserHistory(AioModel):
    """
    Model for storing users' history of selected character in Cassandra DB

    Should be useful for building recomendation system here
    """
    id = columns.UUID(primary_key=True, default=uuid4)
    user_id = columns.Integer()
    character_id = columns.Integer()
    created_at = columns.DateTime(default=datetime.now)
