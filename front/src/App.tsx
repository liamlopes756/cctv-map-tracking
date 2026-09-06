import { Activity, Camera, Database, RadioTower } from "lucide-react";

import { MetricCard } from "./components/MetricCard";
import { LiveViewPage } from "./pages/LiveViewPage";

export function App() {
  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">CCTV</p>
          <h1>Map Tracking</h1>
        </div>
        <nav aria-label="Principal">
          <a className="active" href="#live">
            <Camera size={18} />
            Live view
          </a>
          <a href="#metrics">
            <Activity size={18} />
            Metricas
          </a>
          <a href="#streams">
            <RadioTower size={18} />
            Streams
          </a>
          <a href="#storage">
            <Database size={18} />
            Storage
          </a>
        </nav>
      </aside>
      <section className="workspace">
        <header className="workspace-header">
          <div>
            <p className="eyebrow">MVP</p>
            <h2>Monitoramento em tempo real</h2>
          </div>
          <span className="status">Ambiente local</span>
        </header>
        <section className="metrics-grid" aria-label="Metricas principais">
          <MetricCard label="Pessoas ativas" value="0" />
          <MetricCard label="Cameras online" value="0" />
          <MetricCard label="Eventos/min" value="0" />
        </section>
        <LiveViewPage />
      </section>
    </main>
  );
}
