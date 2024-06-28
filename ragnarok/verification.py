from dataclasses import dataclass
from typing import List

@dataclass
class VerificationResult:
    accuracy_score: float
    consistency_score: float
    relevance_score: float
    semantic_similarity_score: float
    confidence_score: float
    issues: List[str]

    @property
    def overall_score(self) -> float:
        return (self.accuracy_score + self.consistency_score + self.relevance_score + self.semantic_similarity_score) / 4