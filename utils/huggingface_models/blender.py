from .base import make_query

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"


async def inference_blender(payload):
    return await make_query(API_URL, payload)
