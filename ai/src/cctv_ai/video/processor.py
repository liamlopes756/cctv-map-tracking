import time
from collections.abc import Generator

import cv2
from ultralytics import YOLO

from cctv_ai.core.models import TrackEvent
from cctv_ai.core.settings import Settings
from cctv_ai.events.publisher import EventPublisher
from cctv_ai.tracking.tracker import Tracker


class VideoProcessor:
    def __init__(
        self,
        settings: Settings,
        publisher: EventPublisher,
        tracker: Tracker | None = None,
    ) -> None:
        self.settings = settings
        self.publisher = publisher
        self.tracker = tracker or Tracker()
        self._detector = YOLO(settings.model_path)

    def mjpeg_stream(self) -> Generator[bytes, None, None]:
        capture = cv2.VideoCapture(self.settings.video_source)
        frame_number = 0
        started_at = time.monotonic()

        try:
            while True:
                ok, frame = capture.read() if capture.isOpened() else (False, None)
                if not ok:
                    if capture.isOpened():
                        if not capture.set(cv2.CAP_PROP_POS_FRAMES, 0):
                            raise RuntimeError(f"Unable to rewind video source: {self.settings.video_source}")
                        self.tracker.reset()
                        continue
                    raise RuntimeError(f"Unable to open video source: {self.settings.video_source}")

                frame_number += 1
                frame = cv2.resize(frame, (self.settings.stream_width, self.settings.stream_height))
                events = self._events_for_frame(frame, frame_number)

                for event in events:
                    self.publisher.publish_track_event(event)
                    self._draw_event(frame, event)

                elapsed = max(time.monotonic() - started_at, 0.001)
                measured_fps = frame_number / elapsed
                cv2.putText(
                    frame,
                    f"FPS {measured_fps:.1f}",
                    (self.settings.stream_width - 150, 34),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                )

                ok, encoded = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 82])
                if ok:
                    yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + encoded.tobytes() + b"\r\n"

                time.sleep(1 / max(self.settings.stream_fps, 1))
        finally:
            capture.release()

    def _events_for_frame(self, frame, frame_number: int) -> list[TrackEvent]:
        detections: list[tuple[float, float, float, float, float]] = []
        results = self._detector.predict(
            frame,
            classes=[0],
            conf=self.settings.detection_confidence,
            device=self.settings.inference_device,
            verbose=False,
        )
        for result in results:
            if result.boxes is None:
                continue
            for box, confidence in zip(result.boxes.xyxy.cpu().tolist(), result.boxes.conf.cpu().tolist()):
                x1, y1, x2, y2 = box
                detections.append(
                    (
                        float(x1),
                        float(y1),
                        float(x2 - x1),
                        float(y2 - y1),
                        float(confidence),
                    )
                )

        return [
            TrackEvent(
                camera_id=self.settings.camera_id,
                source_uri=self.settings.video_source,
                track_id=track_id,
                frame_number=frame_number,
                x=x,
                y=y,
                width=width,
                height=height,
                confidence=confidence,
            )
            for track_id, x, y, width, height, confidence in self.tracker.assign(detections[:16])
        ]

    def _draw_event(self, frame, event: TrackEvent) -> None:
        pt1 = (int(event.x), int(event.y))
        pt2 = (int(event.x + event.width), int(event.y + event.height))
        label = f"ID {event.track_id}"
        cv2.rectangle(frame, pt1, pt2, (34, 197, 94), 2)
        cv2.rectangle(frame, (pt1[0], max(pt1[1] - 28, 0)), (pt1[0] + 82, pt1[1]), (134, 239, 172), -1)
        cv2.putText(frame, label, (pt1[0] + 6, max(pt1[1] - 8, 16)), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (5, 46, 22), 2)
