using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

namespace Nexus404.Middleware
{
    public class Nexus404Middleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<Nexus404Middleware> _logger;

        public Nexus404Middleware(RequestDelegate next, ILogger<Nexus404Middleware> logger)
        {
            _next = next;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            await _next(context);

            if (context.Response.StatusCode == StatusCodes.Status404NotFound && !context.Response.HasStarted)
            {
                _logger.LogWarning("404 Not Found intercepted for path: {Path}", context.Request.Path);
                
                context.Response.Clear();
                context.Response.StatusCode = StatusCodes.Status404NotFound;
                context.Response.ContentType = "application/json";
                
                var errorResponse = "{\"status\": 404, \"error\": \"Not Found\", \"message\": \"The requested resource was not found.\"}";
                await context.Response.WriteAsync(errorResponse);
            }
        }
    }
}
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.