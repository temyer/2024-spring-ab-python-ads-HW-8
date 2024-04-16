from functools import lru_cache

import pika
import json
import redis

from config import get_config
from train import get_precision_score


@lru_cache
def get_redis() -> redis.Redis:
    config = get_config()

    redis_instance = redis.Redis(
        host=config.REDIS_HOST, port=config.REDIS_PORT, password=config.REDIS_PWD
    )

    return redis_instance


def get_request(request_id):
    request_data = get_redis().get(request_id)
    if request_data:
        return json.loads(request_data)
    return None


def update_request(request_id, status, output):
    request_details = get_request(request_id)
    get_redis().set(
        request_id,
        json.dumps(
            {
                "input": request_details["input"],
                "status": status,
                "output": output,
            }
        ),
    )


def callback(ch, method, properties, body):
    body = json.loads(body)
    request_id = body["request_id"]
    print(f"Received request with ID: {request_id}")
    input = body["input"]

    train_size = input["train_size"]
    approach = input["approach"]

    output = get_precision_score(approach, train_size)

    update_request(request_id, "done", output)


def start_consumer():
    print("starting consumer...")
    config = get_config()

    credentials = pika.PlainCredentials(config.RABBIT_USER, config.RABBIT_PWD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            config.RABBIT_HOST,
            config.RABBIT_PORT,
            credentials=credentials,
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue="train", durable=True)
    channel.basic_consume(queue="train", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == "__main__":
    start_consumer()
