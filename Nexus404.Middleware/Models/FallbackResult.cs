using System.Text.Json.Serialization;

namespace Nexus404.Middleware.Models;

public enum FallbackAction
{
    None,
    Redirect,
    RenderHtml,
    Suggestion
}

public class FallbackResult
{
    [JsonPropertyName("actionType")]
    public FallbackAction ActionType { get; set; }

    [JsonPropertyName("suggestedUrl")]
    public string? SuggestedUrl { get; set; }

    [JsonPropertyName("generatedContent")]
    public string? GeneratedContent { get; set; }

    [JsonPropertyName("confidenceScore")]
    public double ConfidenceScore { get; set; }
}
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.