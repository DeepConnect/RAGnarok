import math
from typing import Dict, List
from collections import Counter

def calculate_confidence(*scores: float) -> float:
    mean = sum(scores) / len(scores)
    variance = sum((x - mean) ** 2 for x in scores) / len(scores)
    std_dev = math.sqrt(variance)
    
    confidence = 1 - (std_dev / mean) if mean > 0 else 0
    return max(0, min(confidence, 1))

def extract_weighted_keywords(question: str, docs: List[str]) -> Dict[str, float]:
    all_text = " ".join([question] + docs)
    words = all_text.lower().split()
    word_counts = Counter(words)
    
    total_words = sum(word_counts.values())
    return {word: count / total_words for word, count in word_counts.items()}

def calculate_semantic_similarity(text1: str, text2: str) -> float:
    # This is a placeholder for semantic similarity calculation
    # In a real implementation, you might use a more sophisticated method
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    return intersection / union if union > 0 else 0