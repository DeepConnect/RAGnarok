import unittest
from ragnarok.core import RAGnarok

class TestRAGnarok(unittest.TestCase):
    def setUp(self):
        self.ragnarok = RAGnarok()

    def test_verify(self):
        rag_response = "The capital of France is Paris."
        context = {
            "question": "What is the capital of France?",
            "retrieved_docs": ["Paris is the capital of France.", "France is a country in Europe."]
        }
        result = self.ragnarok.verify(rag_response, context)
        
        self.assertIsNotNone(result)
        self.assertTrue(0 <= result.accuracy_score <= 1)
        self.assertTrue(0 <= result.consistency_score <= 1)
        self.assertTrue(0 <= result.relevance_score <= 1)
        self.assertTrue(0 <= result.semantic_similarity_score <= 1)
        self.assertTrue(0 <= result.confidence_score <= 1)

if __name__ == '__main__':
    unittest.main()