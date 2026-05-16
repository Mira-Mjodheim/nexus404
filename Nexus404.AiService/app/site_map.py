import os
import json
import logging
import math
from collections import Counter
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def compute_cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        return 0.0
    return float(numerator) / denominator

def get_character_ngrams(text: str, n: int = 3) -> List[str]:
    text = f" {text} "
    return [text[i:i+n] for i in range(len(text)-n+1)]

class SiteMapManager:
    def __init__(self):
        self.routes: List[str] = []
        self.route_metadata: List[Dict[str, Any]] = []
        self.route_vectors: List[Dict[str, float]] = []
        self.idf: Dict[str, float] = {}
        self.is_initialized = False

    def ingest_routes(self, routes_data: List[Dict[str, Any]]) -> None:
        self.routes = []
        self.route_metadata = []
        
        for route in routes_data:
            path = route.get('path')
            if path:
                self.routes.append(path)
                self.route_metadata.append(route)
        
        self._build_index()

    def _build_index(self) -> None:
        if not self.routes:
            logger.warning("No routes to index.")
            self.is_initialized = False
            return
            
        processed_paths = [self._preprocess_path(path) for path in self.routes]
        
        document_freq = Counter()
        all_ngrams = []
        
        for path in processed_paths:
            ngrams = get_character_ngrams(path)
            all_ngrams.append(ngrams)
            unique_ngrams = set(ngrams)
            for ngram in unique_ngrams:
                document_freq[ngram] += 1
                
        num_docs = len(self.routes)
        self.idf = {ngram: math.log(num_docs / (freq + 1)) + 1 for ngram, freq in document_freq.items()}
        
        self.route_vectors = []
        for ngrams in all_ngrams:
            tf = Counter(ngrams)
            vec = {ngram: tf[ngram] * self.idf.get(ngram, 1.0) for ngram in tf}
            self.route_vectors.append(vec)
            
        self.is_initialized = True
        logger.info(f"Successfully indexed {len(self.routes)} routes.")

    def _preprocess_path(self, path: str) -> str:
        return path.replace('/', ' ').replace('-', ' ').replace('_', ' ').strip().lower()

    def _vectorize_query(self, query: str) -> Dict[str, float]:
        processed_query = self._preprocess_path(query)
        ngrams = get_character_ngrams(processed_query)
        tf = Counter(ngrams)
        return {ngram: tf[ngram] * self.idf.get(ngram, 1.0) for ngram in tf}

    def find_best_matches(self, failed_path: str, top_k: int = 3) -> List[Dict[str, Any]]:
        if not self.is_initialized or not self.routes:
            return []

        query_vector = self._vectorize_query(failed_path)
        
        scored_routes = []
        for idx, route_vector in enumerate(self.route_vectors):
            score = compute_cosine_similarity(query_vector, route_vector)
            if score > 0.1:
                scored_routes.append({
                    'path': self.routes[idx],
                    'score': score,
                    'metadata': self.route_metadata[idx]
                })
                
        scored_routes.sort(key=lambda x: x['score'], reverse=True)
        return scored_routes[:top_k]

    def load_from_file(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            logger.error(f"Sitemap file not found: {file_path}")
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.ingest_routes(data)
                elif isinstance(data, dict) and 'routes' in data:
                    self.ingest_routes(data['routes'])
        except Exception as e:
            logger.error(f"Error loading sitemap file: {str(e)}")
[WARNING] --raw-output is enabled. Model output is not sanitized and may contain harmful ANSI sequences (e.g. for phishing or command injection). Use --accept-raw-output-risk to suppress this warning.