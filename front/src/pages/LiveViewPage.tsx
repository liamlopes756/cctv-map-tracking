import { useState } from "react";

const STREAM_URL = import.meta.env.VITE_AI_STREAM_URL ?? "http://localhost:8010/stream.mjpg";

export function LiveViewPage() {
  const [loaded, setLoaded] = useState(false);

  return (
    <section className="live-view" aria-label="Video ao vivo">
      <img
        className="video-feed"
        src={STREAM_URL}
        alt="Camera 01 com bounding boxes e IDs"
        onLoad={() => setLoaded(true)}
        onError={() => setLoaded(false)}
      />
      <div className="video-overlay top-left">Camera 01</div>
      <div className="video-overlay top-right">FPS no vídeo</div>
      <div className="video-stage">
        {!loaded && <span>Conectando ao stream</span>}
      </div>
    </section>
  );
}
