from collections.abc import Iterable

from cctv_ai.core.models import TrackEvent
from cctv_ai.tracking.tracker import Tracker


class VideoProcessor:
    def __init__(self, tracker: Tracker | None = None) -> None:
        self.tracker = tracker or Tracker()

    def process(self, frame_count: int = 1) -> Iterable[TrackEvent]:
        for frame_number in range(frame_count):
            yield from self.tracker.update(frame_number)
