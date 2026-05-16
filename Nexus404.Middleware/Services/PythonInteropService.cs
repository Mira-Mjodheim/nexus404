using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Nexus404.Middleware.Interfaces;

namespace Nexus404.Middleware.Services;

public class PythonInteropService : IAiAnalysisService
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<PythonInteropService> _logger;

    public PythonInteropService(HttpClient httpClient, IConfiguration configuration, ILogger<PythonInteropService> logger)
    {
        _httpClient = httpClient ?? throw new ArgumentNullException(nameof(httpClient));
        _logger = logger ?? throw new ArgumentNullException(nameof(logger));

        var pythonApiUrl = configuration["PYTHON_API_URL"] ?? Environment.GetEnvironmentVariable("PYTHON_API_URL") ?? "http://localhost:5000";
        _httpClient.BaseAddress = new Uri(pythonApiUrl);
    }

    public async Task<string> GetRecommendationAsync(string errorDetails, CancellationToken cancellationToken = default)
    {
        try
        {
            var requestData = new { error = errorDetails };
            var response = await _httpClient.PostAsJsonAsync("/api/recommendations", requestData, cancellationToken);
            
            response.EnsureSuccessStatusCode();

            var result = await response.Content.ReadFromJsonAsync<PythonRecommendationResponse>(cancellationToken: cancellationToken);
            return result?.Recommendation ?? string.Empty;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error occurred while requesting recommendations from the Python API.");
            throw;
        }
    }

    private class PythonRecommendationResponse
    {
        public string? Recommendation { get; set; }
    }
}
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.