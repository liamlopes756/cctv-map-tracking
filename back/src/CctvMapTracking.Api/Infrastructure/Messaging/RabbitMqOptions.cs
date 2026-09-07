namespace CctvMapTracking.Api.Infrastructure.Messaging;

public sealed class RabbitMqOptions
{
    public string Url { get; set; } = "amqp://cctv:cctv@localhost:5672/";
    public string Exchange { get; set; } = "cctv.tracking";
    public string Queue { get; set; } = "track-events";
    public string RoutingKey { get; set; } = "track.events";
}
