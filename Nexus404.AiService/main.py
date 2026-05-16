import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Optional, List

app = FastAPI(title="Nexus404 AI Analysis Service")

class AnalysisRequest(BaseModel):
    path: str
    method: str
    headers: Optional[Dict[str, str]] = None
    queryString: Optional[str] = None
    body: Optional[str] = None

class AnalysisResponse(BaseModel):
    isAnomaly: bool
    confidenceScore: float
    suggestions: List[str]
    reasoning: str
    recommendedAction: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_traffic(request: AnalysisRequest):
    is_anomaly = False
    confidence_score = 0.0
    suggestions = []
    reasoning = "Request appears normal based on pattern analysis."
    recommended_action = "allow"

    path_lower = request.path.lower()
    query_lower = request.queryString.lower() if request.queryString else ""
    body_lower = request.body.lower() if request.body else ""

    if "wp-admin" in path_lower or ".php" in path_lower:
        is_anomaly = True
        confidence_score = 0.85
        suggestions.append("Verify if PHP is expected in this application.")
        reasoning = "Suspicious path targeting PHP or WordPress administration."
        recommended_action = "block"

    if "select" in query_lower and "union" in query_lower:
        is_anomaly = True
        confidence_score = 0.95
        suggestions.append("Immediate review of input validation required.")
        reasoning = "Potential SQL injection attempt detected in query parameters."
        recommended_action = "block"
        
    if "<script>" in body_lower or "javascript:" in body_lower:
        is_anomaly = True
        confidence_score = 0.92
        suggestions.append("Ensure output encoding is enabled.")
        reasoning = "Potential Cross-Site Scripting (XSS) payload in body."
        recommended_action = "block"

    if not is_anomaly and request.method not in ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]:
        is_anomaly = True
        confidence_score = 0.70
        suggestions.append("Review allowed HTTP methods.")
        reasoning = "Uncommon HTTP method used."
        recommended_action = "monitor"

    return AnalysisResponse(
        isAnomaly=is_anomaly,
        confidenceScore=confidence_score if is_anomaly else 0.99,
        suggestions=suggestions,
        reasoning=reasoning,
        recommendedAction=recommended_action
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.