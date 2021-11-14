from dataclasses import dataclass
import dataclasses
from time import time
from typing import Optional
from enum import Enum

class ContentType:
    AUDIO = 'audio'
    TEXT = 'text'
    VIDEO = 'video'
    IMAGE = 'image'


@dataclass
class NLPMessageInput:
    message_id: int
    chat_id: int
    character_id: str
    input_content: str


@dataclass
class NLPMessageOutput(NLPMessageInput):
    output_content: str



@dataclass
class DbChatMessage:
    id: int
    content: str
    content_type: ContentType
    from_user_id: int
    to_user_id: int
    reply_chat_message_id: int


@dataclass
class DbUser:
    id: int
    chat_id: str # telegram_id
    first_name: str
    last_name: str


@dataclass
class DbCharacter:
    id: int
    name: str


@dataclass
class DbCharacterHistory:
    id: int
    user_id: int
    character_id: int
    created_at: Optional[int]

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time()
