# Project Roadmap

**Project:** MedRAG
**Version:** 1.0

---

# Vision

Build a production-grade biomedical Retrieval-Augmented Generation platform demonstrating modern AI engineering best practices.

---

# Sprint 0 — Planning ✅

## Objectives

* Project definition
* Architecture
* API design
* Data model
* Technology selection

**Deliverables**

* Documentation
* Engineering blueprint

---

# Sprint 1 — Development Environment

## Goals

* Repository initialization
* uv setup
* FastAPI skeleton
* Docker
* Ruff
* Black
* mypy
* pytest
* GitHub Actions

**Deliverable**

Production-ready project foundation.

---

# Sprint 2 — Literature Ingestion

## Goals

* PubMed client
* PMC client
* Download pipeline
* Metadata parser
* Storage

**Deliverable**

Reliable biomedical ingestion pipeline.

---

# Sprint 3 — Processing Pipeline

## Goals

* Cleaning
* Chunking
* Metadata extraction
* Token counting

**Deliverable**

Optimized searchable chunks.

---

# Sprint 4 — Embeddings & Indexing

## Goals

* BGE embeddings
* Qdrant integration
* Batch indexing

**Deliverable**

Vector search infrastructure.

---

# Sprint 5 — Hybrid Retrieval

## Goals

* BM25
* Dense retrieval
* Fusion
* Filtering

**Deliverable**

Hybrid retrieval engine.

---

# Sprint 6 — Reranking

## Goals

* BGE reranker
* Ranking optimization
* Retrieval benchmarking

**Deliverable**

High-precision retrieval.

---

# Sprint 7 — Answer Generation

## Goals

* Prompt builder
* LLM integration
* Citation engine

**Deliverable**

Evidence-grounded answer generation.

---

# Sprint 8 — Evaluation

## Goals

* RAGAS
* MLflow
* Benchmarks
* Regression suite

**Deliverable**

Comprehensive evaluation framework.

---

# Sprint 9 — Frontend

## Goals

* Next.js interface
* Search
* Paper viewer
* Citation explorer
* Evaluation dashboard

**Deliverable**

Research-oriented user interface.

---

# Sprint 10 — Production Readiness

## Goals

* Docker optimization
* Deployment
* Performance tuning
* Documentation updates
* Final polish

**Deliverable**

Production-ready MVP.

---

# Success Criteria

By the end of the project, MedRAG should provide:

* Hybrid retrieval
* Citation-backed answers
* Automated evaluation
* Observability
* Modular architecture
* High test coverage
* Docker deployment
* CI/CD pipeline
* Comprehensive documentation

---

# Guiding Principles

Throughout every sprint:

* Build incrementally.
* Measure improvements.
* Keep architecture modular.
* Avoid unnecessary complexity.
* Prioritize maintainability.
* Update documentation alongside implementation.

---

# Post-MVP Vision

Potential future enhancements:

* Multi-modal retrieval
* Knowledge graphs
* Agentic literature review
* Continuous indexing
* Personalized workspaces
* Multi-agent reasoning
* Biomedical workflow automation

---

# Sprint Review Template

Every sprint concludes with:

## Completed

* Objectives achieved

## Metrics

* Performance
* Test coverage
* Benchmarks

## Lessons Learned

* Key takeaways

## Technical Debt

* Known issues

## Next Sprint

* Planned objectives

---

# Summary

This roadmap provides a structured, iterative path toward a production-grade biomedical AI platform. Each sprint delivers a working, testable increment while preserving architectural quality and engineering discipline.
