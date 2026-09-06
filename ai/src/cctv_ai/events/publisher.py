from cctv_ai.core.models import TrackEvent


class EventPublisher:
    def publish_track_event(self, event: TrackEvent) -> None:
        # RabbitMQ integration will be added after the event contract is finalized.
        _ = event
