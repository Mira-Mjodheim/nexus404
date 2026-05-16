using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Nexus404.Middleware;
using Nexus404.Middleware.Interfaces;
using Nexus404.Middleware.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSingleton<IAiAnalysisService, PythonInteropService>();
builder.Services.AddNexus404();

var app = builder.Build();

app.UseNexus404();

app.MapGet("/", () => "Nexus404 Demo App. Try to navigate to an unknown route to test the AI middleware.");

app.Run();
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.