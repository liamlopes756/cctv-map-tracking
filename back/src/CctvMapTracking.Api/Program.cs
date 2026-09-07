using CctvMapTracking.Api.Contracts;
using CctvMapTracking.Api.Infrastructure.Messaging;
using CctvMapTracking.Api.Infrastructure.Persistence;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<RabbitMqOptions>(builder.Configuration.GetSection("RabbitMQ"));
builder.Services.Configure<PostgresOptions>(options =>
{
    options.ConnectionString = builder.Configuration.GetConnectionString("Postgres") ?? string.Empty;
});
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddScoped<ITrackEventRepository, PostgresTrackEventRepository>();
builder.Services.AddHostedService<RabbitMqTrackEventConsumer>();
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy
            .WithOrigins(builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>() ?? ["http://localhost:5173"])
            .AllowAnyHeader()
            .AllowAnyMethod();
    });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors();
app.MapControllers();

app.MapGet("/health", () => Results.Ok(new HealthResponse("ok", "back")))
    .WithName("Health");

app.Run();

public partial class Program;
