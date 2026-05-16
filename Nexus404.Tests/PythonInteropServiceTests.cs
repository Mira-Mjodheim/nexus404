using System;
using System.Net;
using System.Net.Http;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging.Abstractions;
using Nexus404.Middleware.Models;
using Nexus404.Middleware.Services;
using Xunit;

namespace Nexus404.Tests;

public class PythonInteropServiceTests
{
    private class MockHttpMessageHandler : HttpMessageHandler
    {
        private readonly HttpResponseMessage _responseMessage;
        private readonly Exception _exceptionToThrow;

        public MockHttpMessageHandler(HttpResponseMessage responseMessage)
        {
            _responseMessage = responseMessage;
            _exceptionToThrow = null!;
        }

        public MockHttpMessageHandler(Exception exceptionToThrow)
        {
            _exceptionToThrow = exceptionToThrow;
            _responseMessage = null!;
        }

        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            if (_exceptionToThrow != null)
            {
                throw _exceptionToThrow;
            }

            return Task.FromResult(_responseMessage);
        }
    }

    [Fact]
    public async Task AnalyzeErrorAsync_ShouldReturnFallbackResult_WhenApiCallIsSuccessful()
    {
        var expectedResult = new FallbackResult
        {
            SuggestedAction = "ClearCache",
            Confidence = 0.99
        };

        var response = new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent(JsonSerializer.Serialize(expectedResult))
        };

        var httpClient = new HttpClient(new MockHttpMessageHandler(response))
        {
            BaseAddress = new Uri("http://localhost:5000/")
        };

        var logger = NullLogger<PythonInteropService>.Instance;
        var service = new PythonInteropService(httpClient, logger);

        var request = new AnalysisRequest
        {
            ErrorMessage = "Cache miss",
            StatusCode = 404
        };

        var result = await service.AnalyzeErrorAsync(request);

        Assert.NotNull(result);
        Assert.Equal(expectedResult.SuggestedAction, result.SuggestedAction);
        Assert.Equal(expectedResult.Confidence, result.Confidence);
    }

    [Fact]
    public async Task AnalyzeErrorAsync_ShouldReturnNull_WhenApiCallFails()
    {
        var response = new HttpResponseMessage(HttpStatusCode.InternalServerError);

        var httpClient = new HttpClient(new MockHttpMessageHandler(response))
        {
            BaseAddress = new Uri("http://localhost:5000/")
        };

        var logger = NullLogger<PythonInteropService>.Instance;
        var service = new PythonInteropService(httpClient, logger);

        var request = new AnalysisRequest
        {
            ErrorMessage = "Database timeout",
            StatusCode = 500
        };

        var result = await service.AnalyzeErrorAsync(request);

        Assert.Null(result);
    }

    [Fact]
    public async Task AnalyzeErrorAsync_ShouldReturnNull_WhenExceptionIsThrown()
    {
        var httpClient = new HttpClient(new MockHttpMessageHandler(new HttpRequestException("Network failure")))
        {
            BaseAddress = new Uri("http://localhost:5000/")
        };

        var logger = NullLogger<PythonInteropService>.Instance;
        var service = new PythonInteropService(httpClient, logger);

        var request = new AnalysisRequest
        {
            ErrorMessage = "Service unavailable",
            StatusCode = 503
        };

        var result = await service.AnalyzeErrorAsync(request);

        Assert.Null(result);
    }

    [Fact]
    public async Task AnalyzeErrorAsync_ShouldReturnNull_WhenResponseIsInvalidJson()
    {
        var response = new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent("Invalid JSON format")
        };

        var httpClient = new HttpClient(new MockHttpMessageHandler(response))
        {
            BaseAddress = new Uri("http://localhost:5000/")
        };

        var logger = NullLogger<PythonInteropService>.Instance;
        var service = new PythonInteropService(httpClient, logger);

        var request = new AnalysisRequest
        {
            ErrorMessage = "Parsing error",
            StatusCode = 400
        };

        var result = await service.AnalyzeErrorAsync(request);

        Assert.Null(result);
    }
}
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.