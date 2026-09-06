using System.Net;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

namespace CctvMapTracking.Api.Tests;

public sealed class HealthTests
{
    [Fact]
    public async Task Health_ReturnsOk()
    {
        await using var app = new WebApplicationFactory<Program>();
        using var client = app.CreateClient();

        var response = await client.GetAsync("/health");

        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
