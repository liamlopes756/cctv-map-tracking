using CctvMapTracking.Api.Contracts;
using CctvMapTracking.Api.Infrastructure.Persistence;
using Microsoft.AspNetCore.Mvc;

namespace CctvMapTracking.Api.Controllers;

[ApiController]
[Route("api/tracks")]
public sealed class TracksController : ControllerBase
{
    private readonly ITrackEventRepository _repository;

    public TracksController(ITrackEventRepository repository)
    {
        _repository = repository;
    }

    [HttpPost("events")]
    public async Task<IActionResult> ReceiveEvent([FromBody] TrackEventRequest request, CancellationToken cancellationToken)
    {
        await _repository.InsertAsync(request, cancellationToken);
        return Accepted(new { request.CameraId, request.TrackId });
    }
}
