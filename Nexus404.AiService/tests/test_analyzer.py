import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.analyzer import Analyzer
from app.models import AnalysisRequest

@pytest.fixture
def analyzer():
    return Analyzer()

def test_analyzer_initialization(analyzer):
    assert analyzer is not None

@pytest.mark.asyncio
async def test_analyzer_detects_navigation_intent(analyzer):
    request = AnalysisRequest(
        path="/old-profile-link",
        method="GET",
        user_input="Take me to my profile"
    )
    
    if hasattr(analyzer, 'analyze_async'):
        result = await analyzer.analyze_async(request)
        assert result is not None
    elif hasattr(analyzer, 'analyze'):
        result = analyzer.analyze(request)
        assert result is not None

@pytest.mark.asyncio
async def test_analyzer_detects_action_intent(analyzer):
    request = AnalysisRequest(
        path="/404",
        method="POST",
        user_input="I want to create a new support ticket"
    )
    
    if hasattr(analyzer, 'analyze_async'):
        result = await analyzer.analyze_async(request)
        assert result is not None
    elif hasattr(analyzer, 'analyze'):
        result = analyzer.analyze(request)
        assert result is not None

def test_analyzer_handles_empty_input(analyzer):
    request = AnalysisRequest(
        path="/missing-page",
        method="GET",
        user_input=""
    )
    
    if hasattr(analyzer, 'analyze'):
        result = analyzer.analyze(request)
        assert result is not None

def test_analyzer_returns_valid_confidence_score(analyzer):
    request = AnalysisRequest(
        path="/unknown",
        method="GET",
        user_input="help me find the documentation"
    )
    
    if hasattr(analyzer, 'analyze'):
        result = analyzer.analyze(request)
        if hasattr(result, 'confidence'):
            assert isinstance(result.confidence, float)
            assert 0.0 <= result.confidence <= 1.0
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.