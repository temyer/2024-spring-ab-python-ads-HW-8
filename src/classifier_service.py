import json
import uuid

from redis.asyncio import Redis

from src.rabbit import publish_to_rabbitMQ
from src.schemas import ScoreRequest


async def create_request(data: ScoreRequest, redis: Redis):
    random_id = str(uuid.uuid4())
    data = data.model_dump()

    await redis.set(
        random_id,
        json.dumps(
            {
                "input": data,
                "output": "",
                "status": "processing",
            }
        ),
    )

    publish_to_rabbitMQ({"request_id": random_id, "input": data})

    return random_id


async def get_request(request_id: int, redis: Redis):
    request_data = await redis.get(request_id)
    if request_data:
        return json.loads(request_data)
    return None
