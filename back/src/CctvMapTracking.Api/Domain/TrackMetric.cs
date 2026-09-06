namespace CctvMapTracking.Api.Domain;

public sealed class TrackMetric
{
    public required string CameraId { get; init; }
    public required string TrackId { get; init; }
    public required DateTimeOffset ObservedAt { get; init; }
    public required double X { get; init; }
    public required double Y { get; init; }
}
