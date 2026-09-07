using CctvMapTracking.Api.Contracts;
using Microsoft.Extensions.Options;
using Npgsql;

namespace CctvMapTracking.Api.Infrastructure.Persistence;

public sealed class PostgresTrackEventRepository : ITrackEventRepository
{
    private readonly string _connectionString;

    public PostgresTrackEventRepository(IOptions<PostgresOptions> options)
    {
        _connectionString = options.Value.ConnectionString;
    }

    public async Task InsertAsync(TrackEventRequest trackEvent, CancellationToken cancellationToken)
    {
        const string sql = """
            INSERT INTO cameras (id, name, source_uri)
            VALUES (@camera_id, @camera_name, @source_uri)
            ON CONFLICT (id) DO NOTHING;

            INSERT INTO track_metrics (
                camera_id,
                track_id,
                frame_number,
                x,
                y,
                width,
                height,
                confidence
            )
            VALUES (
                @camera_id,
                @track_id,
                @frame_number,
                @x,
                @y,
                @width,
                @height,
                @confidence
            )
            ON CONFLICT (camera_id, track_id, frame_number) DO NOTHING;
            """;

        await using var connection = new NpgsqlConnection(_connectionString);
        await connection.OpenAsync(cancellationToken);

        await using var command = new NpgsqlCommand(sql, connection);
        command.Parameters.AddWithValue("camera_id", trackEvent.CameraId);
        command.Parameters.AddWithValue("camera_name", trackEvent.CameraId);
        command.Parameters.AddWithValue("source_uri", trackEvent.SourceUri);
        command.Parameters.AddWithValue("track_id", trackEvent.TrackId);
        command.Parameters.AddWithValue("frame_number", trackEvent.FrameNumber);
        command.Parameters.AddWithValue("x", trackEvent.X);
        command.Parameters.AddWithValue("y", trackEvent.Y);
        command.Parameters.AddWithValue("width", trackEvent.Width);
        command.Parameters.AddWithValue("height", trackEvent.Height);
        command.Parameters.AddWithValue("confidence", trackEvent.Confidence);

        await command.ExecuteNonQueryAsync(cancellationToken);
    }
}
