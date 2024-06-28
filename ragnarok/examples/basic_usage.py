from ragnarok import RAGnarok

def main():
    checker = RAGnarok()
    rag_response = "The capital of France is Paris. It is known for the Eiffel Tower."
    context = {
        "question": "What is the capital of France?",
        "retrieved_docs": [
            "Paris is the capital and most populous city of France.",
            "France is a country in Western Europe with several overseas regions and territories.",
            "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris."
        ]
    }
    
    result = checker.verify(rag_response, context)
    
    print(f"Overall Score: {result.overall_score:.2f}")
    print(f"Accuracy Score: {result.accuracy_score:.2f}")
    print(f"Consistency Score: {result.consistency_score:.2f}")
    print(f"Relevance Score: {result.relevance_score:.2f}")
    print(f"Semantic Similarity Score: {result.semantic_similarity_score:.2f}")
    print(f"Confidence Score: {result.confidence_score:.2f}")
    print(f"Issues Found: {result.issues}")

if __name__ == "__main__":
    main()