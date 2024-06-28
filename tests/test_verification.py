import unittest
from ragnarok.verification import VerificationResult

class TestVerificationResult(unittest.TestCase):
    def test_overall_score(self):
        result = VerificationResult(
            accuracy_score=0.8,
            consistency_score=0.7,
            relevance_score=0.9,
            semantic_similarity_score=0.85,
            confidence_score=0.75,
            issues=[]
        )
        
        expected_overall_score = (0.8 + 0.7 + 0.9 + 0.85) / 4
        self.assertAlmostEqual(result.overall_score, expected_overall_score)

if __name__ == '__main__':
    unittest.main()