using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Moq;
using Nexus404.Middleware;
using Nexus404.Middleware.Interfaces;
using Nexus404.Middleware.Models;
using Xunit;

namespace Nexus404.Tests;

public class Nexus404MiddlewareTests
{
    [Fact]
    public async Task InvokeAsync_ContinuesPipeline_WhenStatusCodeIsNot404()
    {
        var analysisServiceMock = new Mock<IAiAnalysisService>();
        var middleware = new Nexus404Middleware(
            async context =>
            {
                context.Response.StatusCode = (int)HttpStatusCode.OK;
                await Task.CompletedTask;
            },
            analysisServiceMock.Object
        );

        var context = new DefaultHttpContext();
        await middleware.InvokeAsync(context);

        Assert.Equal((int)HttpStatusCode.OK, context.Response.StatusCode);
        analysisServiceMock.Verify(x => x.AnalyzeMissingPathAsync(It.IsAny<AnalysisRequest>()), Times.Never);
    }

    [Fact]
    public async Task InvokeAsync_InterceptsAndAnalyzes_WhenStatusCodeIs404()
    {
        var analysisServiceMock = new Mock<IAiAnalysisService>();
        analysisServiceMock.Setup(x => x.AnalyzeMissingPathAsync(It.IsAny<AnalysisRequest>()))
            .ReturnsAsync(default(FallbackResult));

        var middleware = new Nexus404Middleware(
            async context =>
            {
                context.Response.StatusCode = (int)HttpStatusCode.NotFound;
                await Task.CompletedTask;
            },
            analysisServiceMock.Object
        );

        var context = new DefaultHttpContext();
        context.Request.Path = "/not-found-page";
        
        await middleware.InvokeAsync(context);

        analysisServiceMock.Verify(x => x.AnalyzeMissingPathAsync(It.IsAny<AnalysisRequest>()), Times.Once);
    }
}
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.