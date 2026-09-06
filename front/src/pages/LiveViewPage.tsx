import { Maximize2, Play } from "lucide-react";

export function LiveViewPage() {
  return (
    <section className="live-view" id="live">
      <div className="live-toolbar">
        <div>
          <p className="eyebrow">Camera 01</p>
          <h3>Fonte MP4 local</h3>
        </div>
        <div className="button-row">
          <button type="button" aria-label="Iniciar stream">
            <Play size={18} />
          </button>
          <button type="button" aria-label="Expandir video">
            <Maximize2 size={18} />
          </button>
        </div>
      </div>
      <div className="video-stage">
        <div className="track-box track-box-a">
          <span>ID 001</span>
        </div>
        <div className="track-box track-box-b">
          <span>ID 002</span>
        </div>
      </div>
    </section>
  );
}
