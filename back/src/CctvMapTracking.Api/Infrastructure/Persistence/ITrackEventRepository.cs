using CctvMapTracking.Api.Contracts;

namespace CctvMapTracking.Api.Infrastructure.Persistence;

public interface ITrackEventRepository
{
    Task InsertAsync(TrackEventRequest trackEvent, CancellationToken cancellationToken);
}
