# Architecture Document

**Project:** MedRAG
**Version:** 0.1.0
**Status:** Sprint 0 – Phase 2
**Owner:** Swapnil

---

# 1. Purpose

This document defines the software architecture of MedRAG. It describes how the system is structured, how components interact, and the principles that govern implementation.

The primary goals are:

* Maintainability
* Scalability
* Modularity
* Testability
* Observability
* Replaceability
* Reproducibility

This document serves as the architectural reference for all future development.

---

# 2. High-Level Architecture

MedRAG follows a layered architecture with clear separation between presentation, application logic, domain logic, and infrastructure.

```text
                    ┌──────────────────────┐
                    │     Next.js UI       │
                    └──────────┬───────────┘
                               │
                        HTTP / REST API
                               │
                    ┌──────────▼───────────┐
                    │      FastAPI         │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  Application Layer   │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │    Domain Layer      │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
  Retrieval Engine      Generation Engine     Evaluation Engine
        │                      │                      │
        ▼                      ▼                      ▼
 Qdrant / BM25          LangChain + LLM      RAGAS + Phoenix
```

---

# 3. Architectural Principles

## Clean Architecture

Business rules must remain independent of frameworks and infrastructure.

## Dependency Inversion

High-level modules must not depend on low-level implementations.

## Hexagonal Architecture

External systems communicate with the application through well-defined interfaces (ports and adapters).

## Single Responsibility

Each module has one clearly defined purpose.

## Open–Closed Principle

Components should be open for extension but closed for modification.

# 3.1 Dependency Injection Strategy

MedRAG follows constructor-based dependency injection to decouple application services from infrastructure implementations.

Application services receive dependencies through constructors rather than creating them internally.

Example:

```python
class AnswerGenerationService:

    def __init__(
        self,
        retriever: Retriever,
        reranker: Reranker,
        llm: LLMProvider,
    ):
        ...
```

Benefits:

* Easier unit testing
* Replaceable implementations
* Improved modularity
* Reduced coupling
* Better adherence to Dependency Inversion Principle

The project intentionally avoids introducing a dedicated dependency injection framework during the MVP. Native Python constructors and FastAPI's dependency system are sufficient.

---

# 3.2 Interface-Oriented Design

Core application logic depends on abstract interfaces rather than concrete implementations.

Examples include:

* Retriever
* Reranker
* EmbeddingProvider
* LLMProvider
* VectorStore
* DocumentRepository

Concrete implementations such as Qdrant, BM25, or LangChain adapters reside in the Infrastructure Layer.

This allows future replacement of technologies without modifying business logic.

Example:

```python
class Retriever(Protocol):
    ...
```

---

# 3.3 Domain Purity

The Domain Layer represents the core business logic of MedRAG.

It must remain independent of:

* FastAPI
* LangChain
* Qdrant
* MLflow
* Phoenix
* Docker
* Pydantic request models

The Domain Layer should contain only concepts intrinsic to the problem domain, including:

* Documents
* Chunks
* Queries
* Retrieval
* Ranking
* Answers
* Citations
* Evaluation

Infrastructure-specific concerns are handled through adapters.

---

# 4. Layered Design

## Presentation Layer

Responsibilities:

* REST API
* Request validation
* Response serialization
* Authentication (future)
* API versioning

Technology:

* FastAPI
* Pydantic

---

## Application Layer

Coordinates workflows across services.

Examples:

* Search workflow
* Question answering
* Literature ingestion
* Evaluation pipeline

This layer contains orchestration but no infrastructure-specific logic.

---

## Domain Layer

Contains core business logic:

* Retrieval strategies
* Chunking policies
* Citation formatting
* Ranking abstractions
* Evaluation interfaces

No external library should be required to understand this layer.

---

## Infrastructure Layer

Provides concrete implementations for:

* Qdrant
* BM25
* LangChain
* MLflow
* Phoenix
* File storage
* PubMed APIs

Infrastructure components are replaceable.

---

# 5. Component Overview

## API

Responsibilities:

* Accept requests
* Validate input
* Return structured responses
* Handle exceptions

---

## Ingestion Service

Responsibilities:

* Download biomedical literature
* Validate metadata
* Persist raw documents

---

## Processing Service

Responsibilities:

* Clean text
* Extract metadata
* Chunk documents
* Prepare indexing artifacts

---

## Embedding Service

Responsibilities:

* Generate embeddings
* Batch processing
* Cache embeddings
* Version models

---

## Vector Store

Responsibilities:

* Store embeddings
* Metadata filtering
* Similarity search
* Collection management

Primary implementation:

* Qdrant

---

## Sparse Retrieval

Responsibilities:

* BM25 indexing
* Keyword retrieval
* Lexical scoring

---

## Hybrid Retrieval Engine

Responsibilities:

* Combine dense and sparse retrieval
* Score normalization
* Candidate fusion
* Top-K selection

---

## Reranking Service

Responsibilities:

* Improve retrieval precision
* Score candidate relevance
* Reorder search results

Primary implementation:

* BGE Reranker

---

## Generation Service

Responsibilities:

* Build prompts
* Call LLM
* Format responses
* Attach citations

---

## Evaluation Service

Responsibilities:

* Run RAGAS
* Compute retrieval metrics
* Store benchmark results

---

## Monitoring Service

Responsibilities:

* Tracing
* Latency measurement
* Prompt logging
* Token accounting

---

# 6. Data Flow

## Literature Ingestion

```text
PubMed
   │
Download
   │
Validation
   │
Cleaning
   │
Chunking
   │
Embedding
   │
Qdrant
```

---

## Query Flow

```text
User Query
      │
FastAPI
      │
Hybrid Retrieval
      │
Reranking
      │
Prompt Builder
      │
LLM
      │
Citation Formatter
      │
Response
```

---

# 7. Request Lifecycle

1. User submits a biomedical question.
2. FastAPI validates the request.
3. Hybrid retriever searches BM25 and Qdrant.
4. Results are merged.
5. Reranker reorders candidates.
6. Prompt builder assembles context.
7. LLM generates an answer.
8. Citations are attached.
9. Evaluation metrics are recorded (optional).
10. Phoenix traces the request.
11. Response is returned.

---

# 8. Repository Structure

```text
medrag/
│
├── docs/
├── configs/
├── data/
│
├── src/
│   ├── api/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   ├── ingestion/
│   ├── processing/
│   ├── retrieval/
│   ├── embeddings/
│   ├── reranking/
│   ├── generation/
│   ├── evaluation/
│   ├── monitoring/
│   └── shared/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── benchmarks/
│
├── docker/
├── scripts/
├── notebooks/
└── .github/
```

---

# 9. Dependency Boundaries

Allowed dependencies:

```text
                 Presentation
                        │
                        ▼
                Application Services
                        │
                        ▼
              Domain Interfaces (Ports)
                        ▲
                        │
          Infrastructure Adapters
```

Rules:

* Domain imports nothing from Infrastructure.
* Application depends only on abstractions.
* Infrastructure implements interfaces defined by the Domain.
* API communicates through the Application layer only.

---

# 10. Configuration Management

Configuration will be centralized using environment variables and version-controlled configuration files.

Categories include:

* API settings
* Database
* Vector store
* Embeddings
* LLM
* Retrieval
* Monitoring
* Logging

No secrets will be hardcoded.

---

# 11. Logging Strategy

All services will emit structured logs.

Each request should include:

* Request ID
* Timestamp
* User query
* Retrieval latency
* Generation latency
* Total latency
* Errors
* Model versions

---

# 12. Error Handling

Errors are categorized into:

* Validation errors
* Retrieval errors
* Indexing errors
* Generation errors
* External API failures
* Configuration errors

Responses should provide meaningful messages while avoiding leakage of internal details.

---

# 13. Security Considerations

* Environment-based secrets
* Input validation
* Dependency pinning
* Least-privilege access
* Secure Docker images
* API rate limiting (future)

---

# 14. Observability

Phoenix will capture:

* Prompt traces
* Retrieval traces
* LLM calls
* Token usage
* Latency
* Exceptions

MLflow will track:

* Experiments
* Metrics
* Artifacts
* Model versions

---

# 15. Scalability Strategy

The architecture should support:

* Independent API scaling
* Distributed vector databases
* Multiple embedding models
* Alternative rerankers
* Multiple LLM providers
* Background ingestion workers

Future scaling should require minimal architectural changes.

---

# 16. Design Patterns

The following patterns will be used where appropriate:

* Repository Pattern
* Strategy Pattern
* Factory Pattern
* Dependency Injection
* Adapter Pattern
* Builder Pattern (prompt construction)
* Facade Pattern (workflow orchestration)

# 16.1 Architectural Rules

The following rules are mandatory throughout development.

## Rule 1

Application Services may depend only on interfaces.

Never instantiate infrastructure implementations directly.

---

## Rule 2

Infrastructure implements Domain interfaces.

The dependency direction must always point inward.

---

## Rule 3

The Domain Layer must never import:

* FastAPI
* LangChain
* Qdrant
* MLflow
* Phoenix

---

## Rule 4

Business logic belongs in Application and Domain layers.

API routes should remain thin.

---

## Rule 5

Infrastructure components should be replaceable with minimal changes to higher-level modules.

---

## Rule 6

Configuration should be injected rather than globally imported wherever practical.

---

## Rule 7

Favor composition over inheritance.

Compose services from smaller abstractions instead of building deep inheritance hierarchies.

---

## Rule 8

Every external dependency should be isolated behind a well-defined interface.

This includes:

* Vector databases
* LLM providers
* Embedding models
* Rerankers
* Evaluation frameworks


---

# 17. Architectural Decision Process

All significant architectural changes must be documented in `07_DECISIONS.md`.

Each decision should record:

* Context
* Options considered
* Selected approach
* Trade-offs
* Expected impact

---

# 18. Future Architecture Evolution

The architecture is designed to support future additions such as:

* Multi-modal retrieval
* Knowledge graphs
* Agentic workflows
* Streaming responses
* Multi-tenant deployments
* Distributed indexing
* Continuous ingestion
* Biomedical reasoning agents

These features should integrate without requiring major restructuring.

---

# 19. Architecture Quality Attributes

| Attribute       | Design Goal                                       |
| --------------- | ------------------------------------------------- |
| Modularity      | Replace individual components independently       |
| Maintainability | Clear separation of concerns                      |
| Scalability     | Horizontal service scaling                        |
| Reliability     | Graceful failure handling                         |
| Testability     | Isolated unit and integration testing             |
| Observability   | End-to-end tracing and metrics                    |
| Performance     | Efficient retrieval and generation                |
| Reproducibility | Version-controlled experiments and configurations |
| Security        | Safe handling of secrets and inputs               |

---

# 20. Architecture Summary

MedRAG is designed as a modular, production-ready AI platform built around clean architectural principles. Every subsystem is independently replaceable, observable, and testable. The architecture prioritizes long-term maintainability and experimentation, enabling the project to evolve from a portfolio application into a scalable biomedical research platform without fundamental redesign.
