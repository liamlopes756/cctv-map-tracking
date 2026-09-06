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
    confidence DOUBLE PRECISION NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_track_metrics_camera_observed_at
    ON track_metrics(camera_id, observed_at DESC);
