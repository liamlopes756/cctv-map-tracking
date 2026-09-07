from math import hypot

from cctv_ai.core.models import TrackEvent


class Tracker:
    def __init__(self) -> None:
        self._next_id = 1
        self._centroids: dict[str, tuple[float, float]] = {}

    def reset(self) -> None:
        self._centroids.clear()

    def assign(self, detections: list[tuple[float, float, float, float, float]]) -> list[tuple[str, float, float, float, float, float]]:
        tracked: list[tuple[str, float, float, float, float, float]] = []
        updated: dict[str, tuple[float, float]] = {}

        for x, y, width, height, confidence in detections:
            cx = x + width / 2
            cy = y + height / 2
            track_id = self._nearest_track(cx, cy, updated)
            if track_id is None:
                track_id = f"{self._next_id:03d}"
                self._next_id += 1

            updated[track_id] = (cx, cy)
            tracked.append((track_id, x, y, width, height, confidence))

        self._centroids = updated
        return tracked

    def _nearest_track(self, cx: float, cy: float, claimed: dict[str, tuple[float, float]]) -> str | None:
        best_id: str | None = None
        best_distance = 80.0

        for track_id, (last_x, last_y) in self._centroids.items():
            if track_id in claimed:
                continue

            distance = hypot(cx - last_x, cy - last_y)
            if distance < best_distance:
                best_id = track_id
                best_distance = distance

        return best_id
