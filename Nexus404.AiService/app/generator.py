import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any

class LLMGenerator:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.api_url = os.environ.get("OPENAI_ENDPOINT", "https://api.openai.com/v1/chat/completions")
        self.model = os.environ.get("LLM_MODEL", "gpt-4")

    def _call_llm(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("API key is not set")
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        req = urllib.request.Request(
            self.api_url,
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("choices", [{}])[0].get("message", {}).get("content", "")
        except urllib.error.URLError as e:
            raise RuntimeError(f"LLM API call failed: {e}")
