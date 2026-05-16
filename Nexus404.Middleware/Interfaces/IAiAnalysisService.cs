using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace Nexus404.Middleware.Interfaces;

public interface IAiAnalysisService
{
    Task<AiAnalysisResult> AnalyzeRequestAsync(RequestData requestData, CancellationToken cancellationToken = default);
}

public class RequestData
{
    public string Path { get; set; } = string.Empty;
    public string Method { get; set; } = string.Empty;
    public IDictionary<string, string> Headers { get; set; } = new Dictionary<string, string>();
    public string Body { get; set; } = string.Empty;
    public string SourceIp { get; set; } = string.Empty;
}

public class AiAnalysisResult
{
    public bool IsMalicious { get; set; }
    public string ThreatType { get; set; } = string.Empty;
    public double ConfidenceScore { get; set; }
    public string Action { get; set; } = string.Empty;
}
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.