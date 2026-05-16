from typing import Optional, Dict, List
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    path: str = Field(..., description="The path that resulted in a 404 error.")
    query_string: Optional[str] = Field(default=None, description="The query string of the request.")
    method: str = Field(default="GET", description="The HTTP method used.")
    headers: Dict[str, str] = Field(default_factory=dict, description="HTTP headers from the original request.")
    body: Optional[str] = Field(default=None, description="The request body, if any.")

class SuggestedRoute(BaseModel):
    url: str = Field(..., description="The suggested alternative URL.")
    confidence: float = Field(..., description="A confidence score between 0.0 and 1.0.")
    reason: Optional[str] = Field(default=None, description="The reason for this suggestion.")

class FallbackResult(BaseModel):
    html_content: str = Field(..., description="The generated HTML content for the custom 404 page.")
    status_code: int = Field(default=404, description="The HTTP status code to return.")
    content_type: str = Field(default="text/html", description="The content type of the response.")
    suggestions: List[SuggestedRoute] = Field(default_factory=list, description="List of suggested alternative routes.")

class SiteMapConfig(BaseModel):
    base_url: str = Field(..., description="The base URL of the website.")
    routes: List[str] = Field(default_factory=list, description="List of known valid routes.")
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.