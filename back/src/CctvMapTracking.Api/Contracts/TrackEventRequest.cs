using System.Text.Json.Serialization;

namespace CctvMapTracking.Api.Contracts;

public sealed record TrackEventRequest(
    [property: JsonPropertyName("camera_id")]
    string CameraId,
    [property: JsonPropertyName("source_uri")]
    string SourceUri,
    [property: JsonPropertyName("track_id")]
    string TrackId,
    [property: JsonPropertyName("frame_number")]
    int FrameNumber,
    [property: JsonPropertyName("x")]
    double X,
    [property: JsonPropertyName("y")]
    double Y,
    [property: JsonPropertyName("width")]
    double Width,
    [property: JsonPropertyName("height")]
    double Height,
    [property: JsonPropertyName("confidence")]
    double Confidence);
