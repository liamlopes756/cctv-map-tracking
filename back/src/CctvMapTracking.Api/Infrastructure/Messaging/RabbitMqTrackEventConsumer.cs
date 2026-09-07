using System.Text;
using System.Text.Json;
using CctvMapTracking.Api.Contracts;
using CctvMapTracking.Api.Infrastructure.Persistence;
using Microsoft.Extensions.Options;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace CctvMapTracking.Api.Infrastructure.Messaging;

public sealed class RabbitMqTrackEventConsumer : BackgroundService
{
    private static readonly JsonSerializerOptions JsonOptions = new(JsonSerializerDefaults.Web);

    private readonly IServiceScopeFactory _scopeFactory;
    private readonly RabbitMqOptions _options;
    private readonly ILogger<RabbitMqTrackEventConsumer> _logger;

    private IConnection? _connection;
    private IModel? _channel;

    public RabbitMqTrackEventConsumer(
        IServiceScopeFactory scopeFactory,
        IOptions<RabbitMqOptions> options,
        ILogger<RabbitMqTrackEventConsumer> logger)
    {
        _scopeFactory = scopeFactory;
        _options = options.Value;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                StartConsumer();
                await Task.Delay(Timeout.Infinite, stoppingToken);
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                return;
            }
            catch (Exception ex)
            {
                _logger.LogWarning(ex, "RabbitMQ consumer unavailable. Retrying in 5 seconds.");
                DisposeRabbit();
                await Task.Delay(TimeSpan.FromSeconds(5), stoppingToken);
            }
        }
    }

    private void StartConsumer()
    {
        var factory = new ConnectionFactory
        {
            Uri = new Uri(_options.Url),
            DispatchConsumersAsync = false,
        };

        _connection = factory.CreateConnection();
        _channel = _connection.CreateModel();
        _channel.ExchangeDeclare(_options.Exchange, ExchangeType.Direct, durable: true);
        _channel.QueueDeclare(_options.Queue, durable: true, exclusive: false, autoDelete: false);
        _channel.QueueBind(_options.Queue, _options.Exchange, _options.RoutingKey);
        _channel.BasicQos(prefetchSize: 0, prefetchCount: 25, global: false);

        var consumer = new EventingBasicConsumer(_channel);
        consumer.Received += (_, args) => HandleMessage(args);
        _channel.BasicConsume(_options.Queue, autoAck: false, consumer);

        _logger.LogInformation("RabbitMQ consumer listening on queue {Queue}.", _options.Queue);
    }

    private void HandleMessage(BasicDeliverEventArgs args)
    {
        if (_channel is null)
        {
            return;
        }

        try
        {
            var json = Encoding.UTF8.GetString(args.Body.Span);
            var trackEvent = JsonSerializer.Deserialize<TrackEventRequest>(json, JsonOptions)
                ?? throw new JsonException("Track event payload is empty.");

            using var scope = _scopeFactory.CreateScope();
            var repository = scope.ServiceProvider.GetRequiredService<ITrackEventRepository>();
            repository.InsertAsync(trackEvent, CancellationToken.None).GetAwaiter().GetResult();

            _channel.BasicAck(args.DeliveryTag, multiple: false);
        }
        catch (JsonException ex)
        {
            _logger.LogError(ex, "Discarding invalid track event from RabbitMQ.");
            _channel.BasicAck(args.DeliveryTag, multiple: false);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to persist track event from RabbitMQ.");
            _channel.BasicNack(args.DeliveryTag, multiple: false, requeue: true);
        }
    }

    public override void Dispose()
    {
        DisposeRabbit();
        base.Dispose();
    }

    private void DisposeRabbit()
    {
        _channel?.Dispose();
        _connection?.Dispose();
        _channel = null;
        _connection = null;
    }
}
