from typing import Dict, List, Any
from .verification import VerificationResult
from .utils import calculate_confidence, extract_weighted_keywords, calculate_semantic_similarity
from .config import DEFAULT_THRESHOLDS

class RAGnarok:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.thresholds = self.config.get('thresholds', DEFAULT_THRESHOLDS)

    def verify(self, rag_response: str, context: Dict[str, Any]) -> VerificationResult:
        accuracy_score = self._calculate_accuracy(rag_response, context)
        consistency_score = self._check_consistency(rag_response, context)
        relevance_score = self._assess_relevance(rag_response, context)
        semantic_similarity_score = self._calculate_semantic_similarity(rag_response, context)
        
        confidence_score = calculate_confidence(accuracy_score, consistency_score, relevance_score, semantic_similarity_score)
        
        issues = self._identify_issues(rag_response, context)
        
        return VerificationResult(
            accuracy_score=accuracy_score,
            consistency_score=consistency_score,
            relevance_score=relevance_score,
            semantic_similarity_score=semantic_similarity_score,
            confidence_score=confidence_score,
            issues=issues
        )

    def _calculate_accuracy(self, rag_response: str, context: Dict[str, Any]) -> float:
        keywords = extract_weighted_keywords(context['question'], context['retrieved_docs'])
        response_keywords = set(rag_response.lower().split())
        
        total_weight = sum(keywords.values())
        matched_weight = sum(keywords[kw] for kw in response_keywords if kw in keywords)
        
        accuracy = matched_weight / total_weight if total_weight > 0 else 0
        return min(accuracy, 1.0)

    def _check_consistency(self, rag_response: str, context: Dict[str, Any]) -> float:
        doc_embeddings = [calculate_semantic_similarity(doc, rag_response) for doc in context['retrieved_docs']]
        return sum(doc_embeddings) / len(doc_embeddings) if doc_embeddings else 0

    def _assess_relevance(self, rag_response: str, context: Dict[str, Any]) -> float:
        return calculate_semantic_similarity(context['question'], rag_response)

    def _calculate_semantic_similarity(self, rag_response: str, context: Dict[str, Any]) -> float:
        if 'expected_response' in context:
            return calculate_semantic_similarity(context['expected_response'], rag_response)
        return max(calculate_semantic_similarity(doc, rag_response) for doc in context['retrieved_docs'])

    def _identify_issues(self, rag_response: str, context: Dict[str, Any]) -> List[str]:
        issues = []
        
        if self.accuracy_score < self.thresholds['accuracy']:
            issues.append("Low accuracy: Response may not accurately reflect retrieved information")
        
        if self.consistency_score < self.thresholds['consistency']:
            issues.append("Low consistency: Response may contradict retrieved information")
        
        if self.relevance_score < self.thresholds['relevance']:
            issues.append("Low relevance: Response may not directly answer the question")
        
        if self.semantic_similarity_score < self.thresholds['semantic_similarity']:
            issues.append("Low semantic similarity: Response may differ significantly from expected content")
        
        return issues