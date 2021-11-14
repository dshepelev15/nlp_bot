from utils.redis import (
    get_connection,
    get_chat_key_for_user_replicas,
    get_user_last_replicas_by_chat_id,
)
from pytest import mark


@mark.asyncio
async def test_get_n_replicates_when_inserted_more_then_n():
    redis = get_connection()

    chat_id = 12345
    key = get_chat_key_for_user_replicas(chat_id)
    for i in range(15):
        await redis.lpush(key, str(i))

    last_user_replicas = await get_user_last_replicas_by_chat_id(chat_id)

    assert len(last_user_replicas) == 3
    assert last_user_replicas == ['12', '13', '14']
