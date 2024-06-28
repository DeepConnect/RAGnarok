# ragnarok.py

from typing import Dict, List, Any, Set
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

@dataclass
class VerificationResult:
    accuracy_score: float
    consistency_score: float
    relevance_score: float
    semantic_similarity_score: float
    issues: List[str]

    @property
    def overall_score(self) -> float:
        return (self.accuracy_score + self.consistency_score + self.relevance_score + self.semantic_similarity_score) / 4

class RAGnarok:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.doc_embeddings = None

    def verify(self, rag_response: str, context: Dict[str, Any]) -> VerificationResult:
        self._build_hnsw_index(context['retrieved_docs'])
        
        accuracy_score = self._calculate_accuracy(rag_response, context)
        consistency_score = self._check_consistency(rag_response, context)
        relevance_score = self._assess_relevance(rag_response, context)
        semantic_similarity_score = self._calculate_semantic_similarity(rag_response, context)
        issues = self._identify_issues(rag_response, context)
        
        return VerificationResult(
            accuracy_score=accuracy_score,
            consistency_score=consistency_score,
            relevance_score=relevance_score,
            semantic_similarity_score=semantic_similarity_score,
            issues=issues
        )

    def _build_hnsw_index(self, documents: List[str]):
        self.doc_embeddings = self.model.encode(documents)
        dimension = self.doc_embeddings.shape[1]
        
        # Create HNSW index
        self.index = faiss.IndexHNSWFlat(dimension, 32)  # 32 is the number of connections per layer
        self.index.hnsw.efConstruction = 40  # Affects index build time and accuracy
        self.index.hnsw.efSearch = 16  # Affects search time and accuracy
        
        self.index.add(self.doc_embeddings.astype('float32'))

    def _calculate_semantic_similarity(self, rag_response: str, context: Dict[str, Any]) -> float:
        rag_embedding = self.model.encode([rag_response]).astype('float32')
        
        if 'expected_response' in context:
            expected_embedding = self.model.encode([context['expected_response']]).astype('float32')
            _, distances = self.index.search(expected_embedding, 1)
            similarity = 1 / (1 + distances[0][0])  # Convert distance to similarity
        else:
            # If no expected response, compare with the most similar retrieved document
            _, distances = self.index.search(rag_embedding, 1)
            similarity = 1 / (1 + distances[0][0])  # Convert distance to similarity
        
        return float(similarity)

    def _calculate_accuracy(self, rag_response: str, context: Dict[str, Any]) -> float:
        keyword_accuracy = self._keyword_accuracy(rag_response, context)
        semantic_similarity = self._calculate_semantic_similarity(rag_response, context)
        
        return 0.5 * keyword_accuracy + 0.5 * semantic_similarity

    def _keyword_accuracy(self, rag_response: str, context: Dict[str, Any]) -> float:
        keywords = self._extract_keywords(context['question'])
        retrieved_keywords = set()
        for doc in context['retrieved_docs']:
            retrieved_keywords.update(self._extract_keywords(doc))
        
        response_keywords = self._extract_keywords(rag_response)
        
        accuracy = len(response_keywords.intersection(retrieved_keywords)) / len(retrieved_keywords) if retrieved_keywords else 0
        return min(accuracy, 1.0)

    def _check_consistency(self, rag_response: str, context: Dict[str, Any]) -> float:
        response_embedding = self.model.encode([rag_response]).astype('float32')
        _, distances = self.index.search(response_embedding, len(context['retrieved_docs']))
        
        # Convert distances to similarities
        similarities = 1 / (1 + distances[0])
        
        return float(np.mean(similarities))

    def _assess_relevance(self, rag_response: str, context: Dict[str, Any]) -> float:
        question_embedding = self.model.encode([context['question']]).astype('float32')
        response_embedding = self.model.encode([rag_response]).astype('float32')
        
        _, distances = self.index.search(question_embedding, 1)
        similarity = 1 / (1 + distances[0][0])
        
        return float(similarity)

    def _identify_issues(self, rag_response: str, context: Dict[str, Any]) -> List[str]:
        issues = []
        
        semantic_similarity = self._calculate_semantic_similarity(rag_response, context)
        if semantic_similarity < 0.5:
            issues.append("Response may be semantically different from the expected answer or retrieved documents")
        
        consistency_score = self._check_consistency(rag_response, context)
        if consistency_score < 0.5:
            issues.append("Response may be inconsistent with the retrieved documents")
        
        relevance_score = self._assess_relevance(rag_response, context)
        if relevance_score < 0.5:
            issues.append("Response may not be relevant to the question")
        
        return issues

    def _extract_keywords(self, text: str) -> Set[str]:
        return set(text.lower().split())

# Usage example
if __name__ == "__main__":
    checker = RAGnarok()
    rag_response = "The capital of France is Paris. It is known for the Eiffel Tower."
    context = {
        "question": "What is the capital of France?",
        "retrieved_docs": [
            "Paris is the capital and most populous city of France.",
            "France is a country in Western Europe with several overseas regions and territories.",
            "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris."
        ],
        "expected_response": "The capital of France is Paris, which is famous for landmarks like the Eiffel Tower."
    }
    
    result = checker.verify(rag_response, context)
    print(f"Overall Score: {result.overall_score:.2f}")
    print(f"Accuracy Score: {result.accuracy_score:.2f}")
    print(f"Consistency Score: {result.consistency_score:.2f}")
    print(f"Relevance Score: {result.relevance_score:.2f}")
    print(f"Semantic Similarity Score: {result.semantic_similarity_score:.2f}")
    print(f"Issues Found: {result.issues}")