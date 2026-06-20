# MedRAG Project Bible

**Version:** 0.1.0
**Status:** Sprint 0 — Phase 0
**Owner:** Swapnil
**Project Type:** Production-grade AI Engineering Portfolio Project

---

# 1. Vision

## Long-Term Vision

MedRAG aims to become a trustworthy biomedical literature intelligence platform that enables researchers and clinicians to retrieve, understand, and synthesize evidence from scientific literature with transparent citations and measurable reliability.

Rather than acting as a generic chatbot, MedRAG is designed as an evidence-grounded AI system where every generated response is traceable to authoritative biomedical sources.

The project emphasizes production engineering, reproducibility, and scientific rigor, making it both a valuable research tool and a showcase of modern AI system design.

---

# 2. Mission

Build an end-to-end Retrieval-Augmented Generation (RAG) platform that:

* retrieves relevant biomedical literature efficiently
* combines lexical and semantic search
* generates citation-backed answers
* evaluates response quality automatically
* exposes observability into every stage of the pipeline
* follows software engineering best practices from day one

---

# 3. Product Philosophy

MedRAG is **not**:

* a PDF chatbot
* a notebook experiment
* a one-off hackathon project
* an LLM wrapper

MedRAG **is**:

* an AI search engine
* a biomedical knowledge assistant
* a modular RAG platform
* an engineering-first system
* an extensible research platform

---

# 4. Core Values

## Evidence First

Every answer should be grounded in retrieved evidence.

---

## Transparency

Every output should explain:

* retrieved documents
* citations used
* confidence indicators (where appropriate)
* retrieval scores (internally)

---

## Reproducibility

Every experiment should be reproducible through:

* versioned datasets
* versioned prompts
* versioned embeddings
* versioned models
* tracked metrics

---

## Modularity

Every component should be replaceable without affecting unrelated parts of the system.

Examples:

* swap embedding models
* replace vector database
* replace reranker
* replace LLM
* replace evaluation framework

without large architectural changes.

---

## Production Over Prototypes

Temporary shortcuts that create long-term technical debt should be avoided.

Prefer maintainable solutions over quick implementations.

---

# 5. Success Metrics

The project is considered successful if it achieves:

## Engineering Metrics

* Clean architecture
* High code readability
* Comprehensive documentation
* High automated test coverage
* CI passing consistently
* Dockerized deployment
* Easy onboarding for contributors

---

## Retrieval Metrics

* Recall@K
* Precision@K
* MRR
* nDCG

---

## Generation Metrics

* Faithfulness
* Answer Relevancy
* Context Precision
* Context Recall
* Hallucination Rate

---

## Operational Metrics

* Retrieval latency
* End-to-end latency
* Indexing speed
* Memory usage
* API response time

---

# 6. Engineering Principles

## Single Responsibility

Each module should have exactly one responsibility.

---

## Dependency Inversion

Business logic should not depend on frameworks.

---

## Separation of Concerns

Separate:

* ingestion
* preprocessing
* chunking
* embeddings
* retrieval
* reranking
* generation
* evaluation
* monitoring

into independent layers.

---

## Configuration Over Hardcoding

No secrets or configurable values should exist inside source code.

Everything should be configurable.

---

## Explicit Is Better Than Implicit

Prefer readable implementations over clever implementations.

---

# 7. Architecture Principles

The architecture follows a layered approach:

```
Presentation Layer
        │
API Layer
        │
Application Layer
        │
Domain Layer
        │
Infrastructure Layer
```

Infrastructure components should never contain business logic.

---

# 8. Repository Organization

```
medrag/

├── docs/
├── src/
│
├── api/
├── ingestion/
├── processing/
├── retrieval/
├── embeddings/
├── reranking/
├── generation/
├── evaluation/
├── monitoring/
│
├── tests/
├── scripts/
├── configs/
├── data/
├── notebooks/
├── docker/
├── .github/
│
├── pyproject.toml
├── README.md
└── LICENSE
```

Future additions should preserve this modular organization.

---

# 9. Coding Standards

## Language

Python 3.12+

---

## Style

* Black formatting
* Ruff linting
* mypy type checking
* meaningful variable names
* descriptive functions
* minimal comments where code is self-explanatory

---

## Type Hints

All public functions require type annotations.

---

## Documentation

Public classes and methods must include docstrings.

Use Google-style docstrings consistently.

---

## Imports

Standard library

↓

Third-party libraries

↓

Local imports

---

# 10. Git Workflow

Main branches:

```
main
develop
```

Feature branches:

```
feature/<feature-name>

bugfix/<bug-name>

docs/<document-name>

experiment/<idea>

refactor/<module>
```

Every pull request should include:

* description
* rationale
* testing notes
* screenshots (if UI changes)

---

# 11. Commit Convention

Use Conventional Commits.

Examples:

```
feat:

fix:

docs:

test:

refactor:

perf:

ci:

build:

chore:
```

Example:

```
feat(retrieval): implement hybrid search

docs(project): add architecture overview

fix(chunking): handle empty documents
```

---

# 12. Documentation Standards

Documentation is treated as production code.

Every major milestone updates:

* architecture
* roadmap
* evaluation plan
* decisions log
* README (when needed)

Documentation should always reflect the current implementation.

---

# 13. Testing Philosophy

Testing is mandatory.

Testing layers:

## Unit Tests

Small isolated functions.

---

## Integration Tests

Interaction between components.

---

## End-to-End Tests

Entire RAG pipeline.

---

## Regression Tests

Ensure future improvements do not reduce quality.

---

## Evaluation Tests

Automated quality assessment using RAG metrics.

---

# 14. Evaluation Philosophy

Evaluation is a first-class citizen.

Every significant change should answer:

Did retrieval improve?

Did answer quality improve?

Did latency change?

Did hallucination increase?

Engineering decisions should be supported by measurable evidence whenever possible.

---

# 15. Observability Principles

Every important stage should expose telemetry.

Examples:

* retrieved chunks
* embedding latency
* reranking latency
* generation latency
* token usage
* prompt versions
* retrieved document IDs

Monitoring should aid debugging, performance tuning, and regression detection.

---

# 16. Experiment Tracking

All experiments should record:

* model
* embedding model
* prompt version
* reranker
* retrieval settings
* evaluation metrics
* timestamp
* git commit hash (where practical)

Experiments should be reproducible from logged artifacts.

---

# 17. Security Principles

Never commit:

* API keys
* tokens
* credentials
* secrets
* production data

Use environment variables for sensitive configuration.

Validate all external inputs.

Pin dependencies where appropriate and monitor for vulnerabilities.

---

# 18. Performance Principles

Optimize only after measuring.

Priority order:

1. Correctness
2. Reliability
3. Maintainability
4. Performance

Benchmark before and after meaningful optimizations.

---

# 19. Definition of Done

A milestone is complete only if:

* functionality works
* tests pass
* documentation updated
* architecture updated (if needed)
* benchmarks recorded (when applicable)
* lint passes
* formatting passes
* type checks pass
* code reviewed
* commit history is clean

---

# 20. Roadmap

## Sprint 0

Project Foundation

---

## Sprint 1

Development Environment

---

## Sprint 2

Biomedical Literature Ingestion

---

## Sprint 3

Document Processing & Chunking

---

## Sprint 4

Embeddings & Indexing

---

## Sprint 5

Hybrid Retrieval

---

## Sprint 6

Reranking

---

## Sprint 7

Answer Generation

---

## Sprint 8

Evaluation Framework

---

## Sprint 9

Research Interface

---

## Sprint 10

Production Deployment

---

# 21. Architectural Decision Records (ADR)

Major engineering decisions should be documented rather than overwritten.

Each ADR should include:

* Context
* Decision
* Alternatives Considered
* Consequences
* Date
* Author

This creates a transparent history of architectural evolution.

---

# 22. Project Non-Goals

The following are intentionally out of scope for the initial version:

* Electronic Health Record integration
* Clinical decision support
* Medical diagnosis
* Fine-tuning foundation models
* Real-time hospital deployment
* Regulatory compliance beyond engineering best practices

These may be explored in future iterations.

---

# 23. Future Vision

Future releases may include:

* Multi-modal biomedical retrieval
* Figure and table understanding
* Knowledge graph integration
* Agentic literature review workflows
* Personalized research workspaces
* Continuous indexing of newly published papers
* Multi-agent evidence synthesis
* Clinical guideline retrieval
* Drug discovery workflow integration
* Citation recommendation
* Semantic research memory

The architecture should evolve without requiring fundamental redesign.

---

# 24. Guiding Principle

> Build systems that engineers can trust, researchers can verify, and future contributors can extend.

Every architectural decision should improve at least one of the following:

* reliability
* transparency
* modularity
* reproducibility
* maintainability
* scientific rigor

If a decision compromises these qualities, reconsider it before implementation.
