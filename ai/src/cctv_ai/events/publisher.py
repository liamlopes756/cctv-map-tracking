import json
import logging
import time
from typing import Any

import pika

from cctv_ai.core.models import TrackEvent
from cctv_ai.core.settings import Settings

logger = logging.getLogger(__name__)


class EventPublisher:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._connection: pika.BlockingConnection | None = None
        self._channel: Any | None = None

    def publish_track_event(self, event: TrackEvent) -> None:
        body = json.dumps(event.model_dump()).encode("utf-8")
        for attempt in range(3):
            channel = self._get_channel()
            if channel is None:
                time.sleep(1)
                continue

            try:
                channel.basic_publish(
                    exchange=self.settings.rabbitmq_exchange,
                    routing_key=self.settings.rabbitmq_routing_key,
                    body=body,
                    properties=pika.BasicProperties(
                        content_type="application/json",
                        delivery_mode=2,
                    ),
                )
                return
            except pika.exceptions.AMQPError as exc:
                logger.warning("RabbitMQ publish failed (attempt %s/3): %s", attempt + 1, exc)
                self._close()

        logger.error("Dropping track event after RabbitMQ publish retries.")

    def _get_channel(self) -> Any | None:
        if self._channel and self._channel.is_open:
            return self._channel

        try:
            self._connection = pika.BlockingConnection(pika.URLParameters(self.settings.rabbitmq_url))
            self._channel = self._connection.channel()
            self._channel.exchange_declare(
                exchange=self.settings.rabbitmq_exchange,
                exchange_type="direct",
                durable=True,
            )
            self._channel.queue_declare(queue=self.settings.rabbitmq_queue, durable=True)
            self._channel.queue_bind(
                exchange=self.settings.rabbitmq_exchange,
                queue=self.settings.rabbitmq_queue,
                routing_key=self.settings.rabbitmq_routing_key,
            )
            return self._channel
        except pika.exceptions.AMQPError as exc:
            logger.warning("RabbitMQ publish unavailable: %s", exc)
            self._close()
            return None

    def _close(self) -> None:
        if self._connection and not self._connection.is_closed:
            self._connection.close()
        self._channel = None
        self._connection = None
