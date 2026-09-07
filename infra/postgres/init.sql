CREATE TABLE IF NOT EXISTS cameras (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    source_uri TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS track_metrics (
    id BIGSERIAL PRIMARY KEY,
    camera_id TEXT NOT NULL REFERENCES cameras(id),
    track_id TEXT NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    frame_number INTEGER NOT NULL,
    x DOUBLE PRECISION NOT NULL,
    y DOUBLE PRECISION NOT NULL,
    width DOUBLE PRECISION NOT NULL,
    height DOUBLE PRECISION NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,
    CONSTRAINT ck_track_metrics_frame_number CHECK (frame_number >= 0),
    CONSTRAINT ck_track_metrics_dimensions CHECK (width > 0 AND height > 0),
    CONSTRAINT ck_track_metrics_confidence CHECK (confidence >= 0 AND confidence <= 1),
    CONSTRAINT uq_track_metrics_event UNIQUE (camera_id, track_id, frame_number)
);

CREATE INDEX IF NOT EXISTS idx_track_metrics_camera_observed_at
    ON track_metrics(camera_id, observed_at DESC);

CREATE INDEX IF NOT EXISTS idx_track_metrics_track_observed_at
    ON track_metrics(track_id, observed_at DESC);
