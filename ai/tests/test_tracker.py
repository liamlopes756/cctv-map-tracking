from cctv_ai.tracking.tracker import Tracker


def detection(x: float, raw_id: int) -> tuple[float, float, float, float, float, int]:
    return (x, 10.0, 40.0, 80.0, 0.9, raw_id)


def test_preserves_formatted_id_for_same_track() -> None:
    tracker = Tracker()

    first = tracker.assign([detection(10.0, 7)])
    second = tracker.assign([detection(14.0, 7)])

    assert first[0][0] == "001"
    assert second[0][0] == "001"


def test_assigns_distinct_ids_to_distinct_tracks() -> None:
    tracker = Tracker()

    tracked = tracker.assign([detection(10.0, 7), detection(100.0, 8)])

    assert [item[0] for item in tracked] == ["001", "002"]


def test_reset_starts_new_ids_without_reusing_previous_session_ids() -> None:
    tracker = Tracker()
    tracker.assign([detection(10.0, 7)])

    tracker.reset()
    tracked = tracker.assign([detection(10.0, 7)])

    assert tracked[0][0] == "002"