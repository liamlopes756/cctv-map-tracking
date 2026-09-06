namespace CctvMapTracking.Api.Domain;

public sealed class Camera
{
    public required string Id { get; init; }
    public required string Name { get; init; }
    public required string SourceUri { get; init; }
}
