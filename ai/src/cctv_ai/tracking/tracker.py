class Tracker:
    def __init__(self) -> None:
        self._ids: dict[int, str] = {}
        self._next_id = 1

    def reset(self) -> None:
        self._ids.clear()

    def assign(self, detections: list[tuple[float, float, float, float, float, int]]) -> list[tuple[str, float, float, float, float, float]]:
        tracked: list[tuple[str, float, float, float, float, float]] = []
        for x, y, width, height, confidence, raw_id in detections:
            track_id = self._ids.setdefault(raw_id, f"{self._next_id:03d}")
            if track_id == f"{self._next_id:03d}":
                self._next_id += 1
            tracked.append((track_id, x, y, width, height, confidence))
        return tracked
