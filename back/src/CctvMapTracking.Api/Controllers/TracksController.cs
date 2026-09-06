using CctvMapTracking.Api.Contracts;
using Microsoft.AspNetCore.Mvc;

namespace CctvMapTracking.Api.Controllers;

[ApiController]
[Route("api/tracks")]
public sealed class TracksController : ControllerBase
{
    [HttpPost("events")]
    public IActionResult ReceiveEvent([FromBody] TrackEventRequest request)
    {
        // Temporary HTTP entrypoint until RabbitMQ consumer is implemented.
        return Accepted(new { request.CameraId, request.TrackId });
    }
}
