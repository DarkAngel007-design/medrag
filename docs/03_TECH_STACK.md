# Technology Stack

**Project:** MedRAG
**Version:** 0.1.0
**Status:** Sprint 0 – Phase 3

---

# 1. Purpose

This document defines the official technology stack for MedRAG, the rationale behind each technology choice, alternatives considered, trade-offs, versioning policy, and future migration strategy.

The objective is to ensure that technology decisions are intentional, reproducible, and maintainable throughout the project's lifecycle.

---

# 2. Selection Principles

Every technology adopted by MedRAG should satisfy most of the following criteria:

* Open source with an active community
* Production-ready and widely adopted
* Strong documentation and ecosystem
* Modular and replaceable
* Good Python interoperability
* Long-term maintainability
* Compatible with containerized deployments
* Suitable for local development and cloud deployment

---

# 3. Core Technology Stack

| Layer               | Technology              | Purpose                 |
| ------------------- | ----------------------- | ----------------------- |
| Language            | Python 3.12+            | Backend development     |
| Package Manager     | `uv`                    | Dependency management   |
| API Framework       | FastAPI                 | REST API                |
| Data Validation     | Pydantic v2             | Request/response models |
| Frontend            | Next.js                 | Research interface      |
| Styling             | Tailwind CSS            | UI styling              |
| LLM Orchestration   | LangChain               | RAG orchestration       |
| Embeddings          | BAAI/bge-m3             | Dense embeddings        |
| Sparse Retrieval    | BM25                    | Lexical retrieval       |
| Vector Database     | Qdrant                  | Vector search           |
| Reranker            | BAAI/bge-reranker-v2-m3 | Result reranking        |
| LLM Provider        | Configurable            | Answer generation       |
| Evaluation          | RAGAS                   | RAG evaluation          |
| Experiment Tracking | MLflow                  | Experiment management   |
| Observability       | Phoenix                 | Tracing and monitoring  |
| Testing             | pytest                  | Automated testing       |
| Linting             | Ruff                    | Static analysis         |
| Formatting          | Black                   | Code formatting         |
| Type Checking       | mypy                    | Static typing           |
| Containerization    | Docker                  | Deployment              |
| CI/CD               | GitHub Actions          | Continuous Integration  |

---

# 4. Backend Framework

## Selected: FastAPI

### Why

* High performance
* Automatic OpenAPI generation
* Native async support
* Excellent typing support
* Strong ecosystem
* Easy dependency injection

### Alternatives Considered

| Alternative | Reason Not Selected                                   |
| ----------- | ----------------------------------------------------- |
| Flask       | Minimal built-in validation, manual API documentation |
| Django      | Monolithic for this use case                          |
| Litestar    | Smaller ecosystem                                     |
| Quart       | Lower community adoption                              |

### Migration Strategy

Application logic should remain framework-independent, enabling migration to another ASGI framework if required.

---

# 5. Package Management

## Selected: `uv`

### Why

* Extremely fast dependency resolution
* Reproducible lockfiles
* Modern Python packaging
* Integrated virtual environment management

### Alternatives

* Poetry
* pip + venv
* PDM

### Decision

`uv` provides the best balance of performance, simplicity, and reproducibility.

---

# 6. Embedding Model

## Selected: BAAI/bge-m3

### Why

* State-of-the-art multilingual retrieval
* Strong dense retrieval performance
* Supports long documents
* Well-suited for hybrid retrieval workflows

### Alternatives

* e5-large
* GTE
* BioClinicalBERT
* BioBERT embeddings

### Trade-offs

While biomedical-specific embedding models exist, `bge-m3` offers an excellent balance between retrieval quality, multilingual support, and ecosystem maturity. The architecture remains model-agnostic, allowing future experimentation.

---

# 7. Vector Database

## Selected: Qdrant

### Why

* High-performance ANN search
* Rich metadata filtering
* REST and gRPC APIs
* Docker-friendly
* Excellent documentation
* Active development

### Alternatives

| Database | Reason Not Selected                     |
| -------- | --------------------------------------- |
| FAISS    | Library only; lacks server capabilities |
| Chroma   | Simpler but less mature operationally   |
| Weaviate | More complex deployment for MVP         |
| Milvus   | Higher operational overhead             |

### Migration Strategy

The retrieval layer communicates through repository interfaces, enabling future migration with minimal business logic changes.

---

# 8. Sparse Retrieval

## Selected: BM25

### Why

* Strong lexical baseline
* Complements dense retrieval
* Interpretable scoring
* Industry-standard information retrieval technique

### Alternatives

* TF-IDF
* SPLADE
* Elasticsearch-only ranking

### Decision

BM25 offers a reliable and efficient sparse retrieval component for hybrid search.

---

# 9. Reranker

## Selected: BAAI/bge-reranker-v2-m3

### Why

* High cross-encoder accuracy
* Strong compatibility with BGE embeddings
* Effective precision improvements

### Alternatives

* Cohere Rerank
* ColBERT
* MonoT5

### Trade-offs

Cross-encoder rerankers introduce additional latency but substantially improve retrieval precision.

---

# 10. LLM Orchestration

## Selected: LangChain

### Why

* Mature ecosystem
* Extensive integrations
* Prompt management
* Retrieval abstractions
* Community adoption

### Alternatives

* LlamaIndex
* Haystack
* Custom orchestration

### Decision

LangChain provides rapid integration while preserving modularity through abstraction layers.

---

# 11. Evaluation Framework

## Selected: RAGAS

### Why

* Designed specifically for RAG systems
* Automated evaluation metrics
* Active development
* Broad community adoption

### Metrics

* Faithfulness
* Answer Relevancy
* Context Precision
* Context Recall

---

# 12. Experiment Tracking

## Selected: MLflow

### Why

* Standard experiment tracking
* Artifact management
* Metric logging
* Model versioning

### Alternatives

* Weights & Biases
* ClearML
* Aim

### Decision

MLflow provides a self-hostable, open-source solution aligned with the project's reproducibility goals.

---

# 13. Observability

## Selected: Phoenix

### Why

* Native support for LLM applications
* Prompt tracing
* Retrieval inspection
* Token usage analysis
* Latency breakdowns

### Alternatives

* Langfuse
* OpenTelemetry (custom)
* Helicone

---

# 14. Testing Stack

| Tool           | Purpose                      |
| -------------- | ---------------------------- |
| pytest         | Unit and integration testing |
| pytest-cov     | Coverage reporting           |
| pytest-asyncio | Async test support           |
| httpx          | API testing                  |

### Coverage Goal

* Minimum: 85%
* Target: 90%+

---

# 15. Code Quality

## Ruff

Primary linter and import sorter.

## Black

Consistent formatting.

## mypy

Static type checking for public interfaces.

## pre-commit

Automated quality checks before commits.

---

# 16. Containerization

## Docker

Provides reproducible development and deployment environments.

## Docker Compose

Used for local orchestration of services such as:

* FastAPI
* Qdrant
* MLflow
* Phoenix

---

# 17. CI/CD

## GitHub Actions

Pipeline stages:

1. Install dependencies
2. Lint
3. Format check
4. Type check
5. Unit tests
6. Integration tests
7. Build Docker image

Future enhancements may include deployment automation and security scanning.

---

# 18. Versioning Policy

* Semantic Versioning (SemVer)
* Dependency pinning via `uv.lock`
* Regular dependency audits
* Documented upgrade path for major versions

---

# 19. Technology Replacement Strategy

Every external dependency should be isolated behind interfaces where practical.

Examples:

* Embedding models
* Vector databases
* Rerankers
* LLM providers
* Evaluation frameworks

This ensures components can evolve without widespread refactoring.

---

# 20. Future Technology Considerations

Potential future integrations include:

* vLLM for optimized inference
* Kubernetes for orchestration
* Redis for caching
* Apache Kafka for event-driven ingestion
* OpenTelemetry for broader observability
* Triton Inference Server for model serving

These are intentionally deferred until justified by project requirements.

---

# 21. Summary

The MedRAG technology stack prioritizes modularity, reproducibility, and production readiness. Each technology has been selected based on technical merit, ecosystem maturity, and long-term maintainability. Architectural boundaries ensure that individual technologies can be replaced with minimal impact on the rest of the system.
