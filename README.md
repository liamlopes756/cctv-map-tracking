# CCTV Map Tracking

Monorepo para uma plataforma de monitoramento por video com deteccao, tracking e metricas em tempo real.

## Modulos

- `ai/`: servico Python para leitura de video, deteccao/tracking, desenho de bounding boxes e emissao de eventos.
- `back/`: API ASP.NET Core para regras de negocio, autenticacao, persistencia e consumo de eventos.
- `front/`: aplicacao React para live view, dashboard e metricas.
- `infra/`: recursos de infraestrutura local, incluindo PostgreSQL e RabbitMQ.

## Execucao inicial

Para subir a aplicação completa:

1. Coloque um vídeo real em `samples/input.mp4`.
2. If this is not the first run, recreate the local infrastructure volumes with
   `docker compose down -v`.
3. Execute `docker compose up --build`.
4. Abra `http://localhost:8088`.

O serviço de IA não gera frames substitutos: sem `samples/input.mp4`, o stream falha explicitamente.
A imagem da IA instala a versão CPU-only do PyTorch e baixa o modelo YOLO uma única vez durante o build.

Cada modulo possui um `README.md` proprio com comandos e organizacao interna.

Fluxo recomendado para desenvolvimento local:

1. Subir dependencias em `infra/`.
2. Executar o backend em `back/`.
3. Executar o servico de IA em `ai/`.
4. Executar o frontend em `front/`.

Consulte [NEXT_STEPS.md](./NEXT_STEPS.md) para os proximos passos de configuracao e evolucao.
