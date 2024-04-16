import typing as tp

import pika
import json

from src.config import get_config


def publish_to_rabbitMQ(data: tp.Any):
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
    channel.basic_publish(exchange="", routing_key="train", body=json.dumps(data))
    connection.close()
