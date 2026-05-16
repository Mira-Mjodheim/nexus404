import unittest
from app.generator import generate_fallback
from app.models import AnalysisRequest, FallbackResult

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.available_routes = [
            "/",
            "/home",
            "/products",
            "/products/laptops",
            "/products/phones",
            "/contact",
            "/about"
        ]

    def test_generate_fallback_with_partial_match(self):
        request = AnalysisRequest(
            original_url="/products/laptops/gaming",
            method="GET",
            headers={"Accept": "text/html"}
        )
        
        result = generate_fallback(request.original_url, self.available_routes)
        
        self.assertIsInstance(result, FallbackResult)
        self.assertEqual(result.original_url, "/products/laptops/gaming")
        self.assertIsNotNone(result.suggested_url)
        self.assertIn(result.suggested_url, self.available_routes)
        self.assertIsNotNone(result.generated_content)
        self.assertTrue(len(result.generated_content) > 0)
        self.assertIsInstance(result.confidence_score, float)
        self.assertTrue(0.0 <= result.confidence_score <= 1.0)

    def test_generate_fallback_with_no_obvious_match(self):
        request = AnalysisRequest(
            original_url="/random/unknown/path/999",
            method="GET",
            headers={}
        )
        
        result = generate_fallback(request.original_url, self.available_routes)
        
        self.assertIsInstance(result, FallbackResult)
        self.assertEqual(result.original_url, "/random/unknown/path/999")
        self.assertIsNotNone(result.suggested_url)
        self.assertIsNotNone(result.generated_content)
        self.assertTrue(0.0 <= result.confidence_score <= 1.0)

    def test_generate_fallback_with_empty_url(self):
        request = AnalysisRequest(
            original_url="",
            method="GET",
            headers={}
        )
        
        result = generate_fallback(request.original_url, self.available_routes)
        
        self.assertIsInstance(result, FallbackResult)
        self.assertIsNotNone(result.suggested_url)

    def test_generate_fallback_with_empty_routes(self):
        request = AnalysisRequest(
            original_url="/test",
            method="GET",
            headers={}
        )
        
        result = generate_fallback(request.original_url, [])
        
        self.assertIsInstance(result, FallbackResult)
        self.assertIsNone(result.suggested_url)
        self.assertTrue(result.confidence_score < 0.5)

if __name__ == "__main__":
    unittest.main()
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.