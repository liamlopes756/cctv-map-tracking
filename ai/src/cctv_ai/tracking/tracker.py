from collections.abc import Iterable

from cctv_ai.core.models import TrackEvent


class Tracker:
    def update(self, frame_number: int) -> Iterable[TrackEvent]:
        # Placeholder until YOLO + ByteTrack/BoT-SORT is integrated.
        _ = frame_number
        return []
