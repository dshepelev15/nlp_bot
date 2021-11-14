import asyncio

import aioredis
from utils import config

N = 3

async def get_user_last_replicas_by_chat_id(chat_id):
    key = get_chat_key_for_user_replicas(chat_id)
    return await get_n_replicas_by_key(key)


async def get_user_last_generated_replicas_by_chat_id(chat_id):
    key = get_chat_key_for_generated_replicas(chat_id)
    return await get_n_replicas_by_key(key)


async def get_n_replicas_by_key(key):
    redis = get_connection()
    await redis.ltrim(key, 0, N - 1)

    result = await redis.lrange(key, 0, -1)
    return [replica.decode() for replica in result][::-1] # put it in right order


async def save_user_replica(chat_id, replica):
    key = get_chat_key_for_user_replicas(chat_id)
    return await save_replica_by_key(key, replica)


async def save_user_generated_replica(chat_id, replica):
    key = get_chat_key_for_generated_replicas(chat_id)
    return await save_replica_by_key(key, replica)


async def save_replica_by_key(key, replica):
    """
        Save and store in redis N last replicas
    """
    redis = get_connection()
    await redis.lpush(key, replica)
    return await redis.ltrim(key, 0, N - 1)


def get_chat_key_for_user_replicas(chat_id):
    return f'user_replicas:chats:{chat_id}'


def get_chat_key_for_generated_replicas(chat_id):
    return f'generated_replicas:chats:{chat_id}'


_connection = None

def get_connection():
    global _connection
    if _connection is None:
        _connection = aioredis.from_url(f"redis://{config.REDIS_HOSTNAME}")

    return _connection
