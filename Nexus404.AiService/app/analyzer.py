import difflib
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    url: str
    available_routes: Optional[List[str]] = None
    context: Optional[Dict[str, Any]] = None

class FallbackResult(BaseModel):
    suggested_url: Optional[str] = None
    confidence: float = 0.0
    reasoning: str = ""
    is_resolved: bool = False

class SemanticAnalyzer:
    def __init__(self) -> None:
        self.confidence_threshold = 0.45

    def _extract_keywords(self, url: str) -> set[str]:
        clean_url = re.sub(r'^/|/$', '', url.lower())
        parts = re.split(r'[^a-z0-9]+', clean_url)
        return set(p for p in parts if p)

    def analyze(self, request: AnalysisRequest) -> FallbackResult:
        if not request.available_routes:
            return FallbackResult(
                suggested_url=None,
                confidence=0.0,
                reasoning="No available routes provided for semantic matching.",
                is_resolved=False
            )
        
        target_url = request.url.lower().strip()
        target_keywords = self._extract_keywords(target_url)
        
        best_match = None
        highest_score = 0.0
        
        for route in request.available_routes:
            route_lower = route.lower().strip()
            
            if target_url == route_lower:
                return FallbackResult(
                    suggested_url=route,
                    confidence=1.0,
                    reasoning="Exact match found.",
                    is_resolved=True
                )
            
            seq_matcher = difflib.SequenceMatcher(None, target_url, route_lower)
            similarity = seq_matcher.ratio()
            
            route_keywords = self._extract_keywords(route_lower)
            if target_keywords and route_keywords:
                common_keywords = target_keywords.intersection(route_keywords)
                keyword_score = len(common_keywords) / max(len(target_keywords), len(route_keywords))
            else:
                keyword_score = 0.0
                
            combined_score = (similarity * 0.4) + (keyword_score * 0.6)
            
            if combined_score > highest_score:
                highest_score = combined_score
                best_match = route
                
        if best_match and highest_score >= self.confidence_threshold:
            return FallbackResult(
                suggested_url=best_match,
                confidence=round(highest_score, 2),
                reasoning=f"Semantic matching identified '{best_match}' as the closest intent.",
                is_resolved=True
            )
            
        return FallbackResult(
            suggested_url=None,
            confidence=round(highest_score, 2),
            reasoning="Could not find a semantic match with sufficient confidence.",
            is_resolved=False
        )

analyzer_instance = SemanticAnalyzer()

def analyze_intent(request: AnalysisRequest) -> FallbackResult:
    return analyzer_instance.analyze(request)
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.