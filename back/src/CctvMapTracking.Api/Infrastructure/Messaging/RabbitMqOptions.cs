namespace CctvMapTracking.Api.Infrastructure.Messaging;

public sealed class RabbitMqOptions
{
    public string Url { get; init; } = "amqp://guest:guest@localhost:5672/";
}
