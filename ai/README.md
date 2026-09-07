# AI Module

Servico Python responsavel por processar video, executar deteccao/tracking e publicar eventos para o backend.

## Organizacao

- `run.py`: ponto de entrada simples para execucao local.
- `pyproject.toml`: configuracao do pacote Python e dependencias iniciais.
- `src/cctv_ai/app.py`: fabrica da aplicacao FastAPI.
- `src/cctv_ai/main.py`: entrada via modulo Python.
- `src/cctv_ai/api/`: rotas HTTP de status e controle.
- `src/cctv_ai/core/`: configuracoes e modelos compartilhados.
- `src/cctv_ai/video/`: leitura e processamento de frames.
- `src/cctv_ai/tracking/`: associacao dos deteccoes de pessoas para IDs persistentes.
- `src/cctv_ai/events/`: publicacao dos eventos de tracking para RabbitMQ.
- `tests/`: testes do modulo.

## Execucao

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
python run.py
```

API local: `http://localhost:8010`

O MVP usa `yolo11n.pt` para detectar somente a classe `person` (classe 0 do
modelo COCO) e faz a associacao dos deteccoes entre frames para gerar IDs.
O arquivo MP4 e reiniciado automaticamente no fim para manter o stream em loop.
