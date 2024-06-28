import unittest
from ragnarok.utils import calculate_confidence, extract_weighted_keywords, calculate_semantic_similarity

class TestUtils(unittest.TestCase):
    def test_calculate_confidence(self):
        confidence = calculate_confidence(0.8, 0.7, 0.9, 0.85)
        self.assertTrue(0 <= confidence <= 1)

    def test_extract_weighted_keywords(self):
        question = "What is the capital of France?"
        docs = ["Paris is the capital of France.", "France is a country in Europe."]
        keywords = extract_weighted_keywords(question, docs)
        
        self.assertIn("capital", keywords)
        self.assertIn("france", keywords)

    def test_calculate_semantic_similarity(self):
        text1 = "The quick brown fox jumps over the lazy dog"
        text2 = "A fast brown fox leaps over a sleepy dog"
        similarity = calculate_semantic_similarity(text1, text2)
        
        self.assertTrue(0 <= similarity <= 1)
        self.assertGreater(similarity, 0.5)  # These sentences are quite similar

if __name__ == '__main__':
    unittest.main()