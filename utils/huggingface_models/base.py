from logging import log
import httpx
import logging

from utils import config

headers = {"Authorization": f"Bearer {config.HUGGING_FACE_API_TOKEN}"}

async def make_query(api_url, payload):
    async with httpx.AsyncClient() as client:
        logging.info("Send request to huggingface api %s", payload)
        response = await client.post(api_url, headers=headers, json=payload)
        json_response = response.json()
        logging.info('Response from huggingface api %s', json_response)
        return json_response
