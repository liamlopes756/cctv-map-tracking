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
- `src/cctv_ai/tracking/`: contrato do tracker e implementacao stub inicial.
- `src/cctv_ai/events/`: publicacao futura de eventos para RabbitMQ.
- `tests/`: testes do modulo.

## Execucao

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
python run.py
```

API local: `http://localhost:8010`
