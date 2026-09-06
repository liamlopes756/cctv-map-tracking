# Infra Module

Infraestrutura local para desenvolvimento do monorepo.

## Organizacao

- `docker-compose.yml`: sobe PostgreSQL e RabbitMQ.
- `postgres/init.sql`: cria database/schema inicial para metricas.
- `rabbitmq/definitions.json`: reservado para exchanges, queues e bindings.

## Execucao

```powershell
docker compose up -d
```

Servicos:

- PostgreSQL: `localhost:5432`
- RabbitMQ AMQP: `localhost:5672`
- RabbitMQ Management: `http://localhost:15672`
