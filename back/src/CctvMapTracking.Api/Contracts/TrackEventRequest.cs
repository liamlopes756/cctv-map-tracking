namespace CctvMapTracking.Api.Contracts;

public sealed record TrackEventRequest(
    string CameraId,
    string TrackId,
    int FrameNumber,
    double X,
    double Y,
    double Width,
    double Height,
    double Confidence);
