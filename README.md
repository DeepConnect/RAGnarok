
# RAGnarok

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)

![RAGnarok Banner](https://github.com/DeepConnect/RAGnarok/assets/29411278/972cd800-4f25-43b5-ae65-91d8c7fc1917)

RAGnarok: Unleash the power of truth in your Retrieval-Augmented Generation systems!

# RAGnarok

RAGnarok is an open-source framework for verifying and enhancing the accuracy of Retrieval-Augmented Generation (RAG) systems. It uses advanced NLP techniques and efficient similarity search to provide comprehensive assessments of RAG-generated responses.

## Features

- Semantic similarity checking using FAISS HNSW for efficient vector search
- Accuracy assessment combining keyword matching and semantic similarity
- Consistency checking against retrieved documents
- Relevance assessment to the original question
- Issue identification for potential problems in responses
- Overall scoring system for quick quality assessment

## Installation

```bash
pip install ragnarok
```

Note: RAGnarok requires Python 3.7+.

## Dependencies

RAGnarok depends on the following libraries:
- sentence-transformers
- faiss-cpu (or faiss-gpu for GPU support)
- numpy

You can install these dependencies using:

```bash
pip install sentence-transformers faiss-cpu numpy
```

## Usage

Here's a basic example of how to use RAGnarok:

```python
from ragnarok import RAGnarok

checker = RAGnarok()
result = checker.verify(rag_response, context)
print(f"Overall Score: {result.overall_score:.2f}")
```

## Configuration

RAGnarok can be configured by passing a configuration dictionary when initializing:

```python
from ragnarok import RAGnarok

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
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

## License

RAGnarok is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Citation

If you use RAGnarok in your research, please cite:

```
@software{ragnarok,
  title = {RAGnarok: A Framework for Verifying Retrieval-Augmented Generation},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/yourusername/ragnarok}
}
```

## Contact

For any questions or feedback, please open an issue on GitHub or contact [KnightOwl](mailto:rahulkumar2312016@gmail.com).
