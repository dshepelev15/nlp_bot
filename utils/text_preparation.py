from utils.redis import (
    get_user_last_replicas_by_chat_id,
    get_user_last_generated_replicas_by_chat_id,
    save_user_generated_replica,
    save_user_replica,
)

TOKEN_LIMIT = 100

async def get_prepared_huggingface_payload(chat_id, current_replica):
    previous_user_replicas = await get_user_last_replicas_by_chat_id(chat_id)
    previous_generated_replicates = await get_user_last_generated_replicas_by_chat_id(chat_id)

    return {
        "inputs": {
            "past_user_inputs": get_filtered_context(previous_user_replicas),
            "generated_responses": get_filtered_context(previous_generated_replicates),
            "text": get_filtered_replica(current_replica),
        }
    }


async def save_huggingface_response_and_get_generated_replica(chat_id, current_replica, response):
    generated_text = response['generated_text']
    await save_user_replica(chat_id, get_filtered_replica(current_replica))
    await save_user_generated_replica(chat_id, generated_text)
    return generated_text


def get_filtered_context(previous_user_replicas):
    """
    will take only 100 Tokens from all replicas
    """
    result = []
    token_count = 0
    for previous_user_replica in previous_user_replicas:
        filtered_tokens = [token for token in previous_user_replica.split(' ') if token.strip()]
        if len(filtered_tokens) == 0:
            continue

        if len(filtered_tokens) + token_count < TOKEN_LIMIT:
            token_count += len(filtered_tokens)
            result.append(' '.join(filtered_tokens))
        else:
            filtered_tokens = [token for token in filtered_tokens[:TOKEN_LIMIT - token_count] if token.strip()]
            result.append(' '.join(filtered_tokens))
            break

    return result


def get_filtered_replica(replica):
    return ' '.join(replica.split(' ')[:TOKEN_LIMIT])